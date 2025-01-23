import time

import aiohttp
import jwt
import os
from settings import *
from dotenv import load_dotenv

load_dotenv()

# BASE_URL = "http://194.35.13.58/"
# CHECK_PEOPLE_HAS_QRCODE_URL = BASE_URL + "api/v1/people/IDs/?format=json"
# CHECK_QRCODE_URL = BASE_URL + "api/v1/qrcode/check/"
#
# QRCODES_PATH = 'images/qr_codes/'


class JWTManager:
    def __init__(self):
        self.token_url = ACCESS_TOKEN_URL
        self.refresh_url = REFRESH_TOKEN_URL
        self.username = "kreativpark_bot"
        self.password = os.getenv("PASSWORD")
        self.access_token = None
        self.refresh_token = None

    async def obtain_tokens(self):
        """
        Obtain the access and refresh tokens by making an authentication request.
        """
        print({"username": self.username, "password": self.password})

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=self.token_url,
                json={"username": self.username, "password": self.password},
            )

        print(await response.json())

        if response.status == 200:
            tokens = await response.json()
            self.access_token = tokens["access"]
            self.refresh_token = tokens["refresh"]
            print("Tokens obtained successfully.")
        else:
            raise Exception("Failed to obtain tokens.")

    async def refresh_access_token(self):
        """
        Refresh the access token using the refresh token.
        """
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.refresh_url, json={"refresh": self.refresh_token})

        if response.status == 200:
            self.access_token = response.json()["access"]
            print("Access token refreshed successfully.")
        elif response.status == 401:
            print("Refresh token expired, obtaining new tokens...")
            await self.obtain_tokens()
        else:
            raise Exception("Failed to refresh access token.")

    def is_token_expired(self):
        """
        Check if the access token is expired by decoding the 'exp' field.
        """
        try:
            decoded_token = jwt.decode(
                self.access_token, options={"verify_signature": False}
            )
            exp_timestamp = decoded_token.get("exp")

            if exp_timestamp:
                current_timestamp = time.time()
                if exp_timestamp < current_timestamp:
                    return True
            return False
        except jwt.DecodeError:
            return True

    async def make_request(self, url, method="GET", data=None):
        """
        Make a request using the access token. Check if token is expired before the request.
        """
        if self.is_token_expired():
            print("Access token expired, refreshing token...")
            await self.refresh_access_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = None
        if method == "POST":
            async with aiohttp.ClientSession() as session:
                response = await session.post(url, headers=headers, json=data)
        elif method == "GET":
            async with aiohttp.ClientSession() as session:
                response = await session.get(url, headers=headers, params=data)

        return response


async def get_req(url: str, jwt_manager: JWTManager, data=None) -> aiohttp.ClientResponse:
    return await jwt_manager.make_request(url, "GET", data)


async def post_req(url: str, jwt_manager: JWTManager, obj: dict) -> aiohttp.ClientResponse:
    return await jwt_manager.make_request(url, "POST", obj)
