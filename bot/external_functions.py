from bot_instance import bot_tocken
import requests


def send_telegram_message(text, user_id):
    print('send_telegram_message works ! ')
    url = f"https://api.telegram.org/bot{bot_tocken}/sendMessage"
    payload = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
