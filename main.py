from func import check_url_register
from bot_tele import send_telegram_message
from dict_api import dict_api_url
import time
from datetime import datetime


def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key = "hanoi_b1"
    api_url = dict_api_url[key]
    urls = check_url_register(api_url)
    if urls:
        url = urls[0]
        message = (
            "Github Action - Goethe hiện link đăng ký ~ Vũ Quang Cường: 0354449090\n"
            + url
        )
        message_with_time = f"{message} - {current_time}"
        send_telegram_message(message_with_time)
    else:
        message = (
            "Github Action - Không tìm thấy link đăng ký ~ Vũ Quang Cường: 0354449090\n"
        )
        message_with_time = f"{message} - {current_time}"
        send_telegram_message(message_with_time)


if __name__ == "__main__":
    main()
