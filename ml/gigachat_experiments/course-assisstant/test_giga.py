from gigachat import GigaChat
from gigachat_client import get_gigachat_token

with GigaChat(access_token=get_gigachat_token(), verify_ssl_certs=False) as giga:
    resp = giga.chat("Привет! Кто ты?")
    print(resp.choices[0].message.content)