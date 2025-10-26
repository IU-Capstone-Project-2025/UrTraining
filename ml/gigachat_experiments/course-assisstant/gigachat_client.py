import aiohttp
import requests
import base64
import uuid
import os
from gigachat import GigaChat

def get_gigachat_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    client_id = os.getenv("GIGACHAT_CLIENT_ID", "01997770-cc27-7fe1-90b2-88fa43a8b72d")
    client_secret = os.getenv("GIGACHAT_CLIENT_SECRET", "19d6edd6-7038-4c72-837b-3df65cfc8f9a")

    if not client_id or not client_secret:
        raise ValueError("Missing GIGACHAT_CLIENT_ID or GIGACHAT_CLIENT_SECRET environment variables")

    auth_str = f"{client_id}:{client_secret}".encode("utf-8")
    b64_auth = base64.b64encode(auth_str).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {b64_auth}",
    }

    data = {"scope": "GIGACHAT_API_PERS"}

    response = requests.post(url, headers=headers, data=data, verify=False)

    if response.status_code != 200:
        print("❌ GigaChat token request failed:", response.status_code, response.text)
        response.raise_for_status()

    token_data = response.json()
    print("Access token:", token_data["access_token"])
    return token_data["access_token"]

def get_gigachat_client():
    # verify_ssl_certs=False — чтобы не падало на самоподписанных сертификатах
    return GigaChat(
        access_token=get_gigachat_token(),
        verify_ssl_certs=False
    )
