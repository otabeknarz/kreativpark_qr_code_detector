import cv2
from pyzbar.pyzbar import decode
import time
import functions
import settings
import pygame


def run_qrcode_reader():
    cam = cv2.VideoCapture(0)
    cam.set(5, 640)
    cam.set(6, 480)

    pygame.mixer.init()

    alert_sound = pygame.mixer.Sound("sounds/alert.mp3")
    welcome_sound = pygame.mixer.Sound("sounds/welcome.wav")

    camera = True

    while camera:
        success, frame = cam.read()

        for i in decode(frame):
            qrcode_ID = i.data.decode("utf-8")
            try:
                check_qrcode = functions.get_req(functions.CHECK_QRCODE_URL + qrcode_ID)
            except Exception as e:
                print(e)
                print("Internet bilan muammo")
                alert_sound.play()
                time.sleep(2)
                continue

            try:
                qrcode_json_data: dict = check_qrcode.json()
                is_qrcode = True
            except Exception as e:
                print(e)
                print("BUNDAY QRCODE YO'Q")
                alert_sound.play()
                is_qrcode = False

            if is_qrcode:
                if qrcode_json_data["status"] == "true":
                    try:
                        res = functions.get_req(
                            settings.LOGIN_LIBRARY
                            + qrcode_json_data["qrcode"]["ID"],
                        )
                    except Exception as e:
                        print(e)
                        print("Internet bilan muammo")
                        alert_sound.play()
                        time.sleep(2)
                        continue
                    json_data = res.json()
                    if res.status_code == 200 and json_data["status"] == "true":
                        print("Kirish mumkin: ", i.data.decode("utf-8"))
                        welcome_sound.play()

                else:
                    print("YANGI QRCODE OLING")
                    alert_sound.play()

                time.sleep(2)

        cv2.imshow("QR Code Reader", frame)
        cv2.waitKey(3)


def main():
    # jwt_manager = functions.JWTManager()
    # await jwt_manager.obtain_tokens()
    print("Running main script")
    run_qrcode_reader()


if __name__ == "__main__":
    main()
