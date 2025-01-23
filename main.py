import cv2
from pyzbar.pyzbar import decode
import time
import asyncio
import functions
import settings
import pygame


async def run_qrcode_reader(jwt_manager: functions.JWTManager):
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
                check_qrcode = await functions.get_req(functions.CHECK_QRCODE_URL + qrcode_ID, jwt_manager)
            except Exception as e:
                print(e)
                print("Internet bilan muammo")
                alert_sound.play()
                time.sleep(2)
                continue

            try:
                qrcode_json_data: dict = await check_qrcode.json()
                is_qrcode = True
            except Exception as e:
                print("BUNDAY QRCODE YO'Q")
                alert_sound.play()
                is_qrcode = False

            if is_qrcode:
                if qrcode_json_data["status"] == "true":
                    try:
                        res = await functions.get_req(
                            settings.LOGIN_LIBRARY
                            + qrcode_json_data["qrcode"]["ID"],
                            jwt_manager,
                        )
                    except:
                        print("Internet bilan muammo")
                        alert_sound.play()
                        time.sleep(2)
                        continue
                    json_data = await res.json()
                    if res.status == 200 and json_data["status"] == "true":
                        print("Kirish mumkin: ", i.data.decode("utf-8"))
                        welcome_sound.play()

                else:
                    print("YANGI QRCODE OLING")
                    alert_sound.play()

                time.sleep(2)

        cv2.imshow("QR Code Reader", frame)
        cv2.waitKey(3)


async def main():
    jwt_manager = functions.JWTManager()
    await jwt_manager.obtain_tokens()
    await run_qrcode_reader(jwt_manager)


if __name__ == "__main__":
    asyncio.run(main())
