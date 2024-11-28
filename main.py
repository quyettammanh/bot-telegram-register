from func import check_url_register
from bot_tele import send_telegram_message

def main():
    # Định nghĩa API mẫu (thay bằng URL API thực tế của bạn)
    api_url = "https://www.goethe.de/rest/examfinder/exams/institute/O%2010000610?category=E015&type=JU&countryIsoCode=vn&locationName=&count=10&start=1&langId=134&timezone=54&isODP=0&sortField=startDate&sortOrder=ASC&dataMode=0&langIsoCodes=de%2Cen%2Cvi"
    
    # Gọi hàm check_url_register
    urls = check_url_register(api_url)
    # # In kết quả
    if urls:
        url=urls[0]
        message='Goethe hiện link đăng ký ~ Vũ Quang Cường: 0354449090\n'+url
        print(message)
        send_telegram_message(message)
    else:
        print("Không tìm thấy URL đăng ký hoặc có lỗi xảy ra.")

# Gọi hàm main để chạy chương trình
if __name__ == "__main__":
    main()