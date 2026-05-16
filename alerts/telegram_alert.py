# alerts/telegram_alert.py
import os
from dotenv import load_dotenv



import requests
load_dotenv()
BOT_TOKEN = "89681xxxxxxxxxxxx"
CHAT_ID = "11xxxxxxxxxx"

def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    return response.status_code
