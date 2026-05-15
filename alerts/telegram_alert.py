# alerts/telegram_alert.py

import requests

BOT_TOKEN = "8968102799:AAFUg3qCRa7-WjK6xICUadq1WlfmHpxj0-I"
CHAT_ID = "1188460670"

def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    return response.status_code