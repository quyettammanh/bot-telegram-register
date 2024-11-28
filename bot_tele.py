import os
import requests
from dotenv import load_dotenv

# Tải các biến môi trường từ file `.env`
load_dotenv()

# Lấy `BOT_TOKEN` và `CHAT_ID` từ biến môi trường
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    """
    Gửi tin nhắn đến Telegram bot.
    :param message: Nội dung tin nhắn.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Gửi yêu cầu POST
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error: {response.status_code}, {response.text}")