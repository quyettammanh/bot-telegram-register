import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from bot_tele import send_telegram_message
import os

def get_proxies(file_path):
    # Đọc nội dung tệp proxy_free.txt
    with open(file_path, 'r', encoding='utf-8') as file:
        proxy_text = file.read()
    
    # Chuyển đổi chuỗi proxy_text thành danh sách các đối tượng proxy
    proxies = []
    for line in proxy_text.strip().split("\n"):
        parts = line.split(":")
        ip = parts[0]
        port = parts[1]
        if len(parts) == 2:  # Trường hợp không có username và password
            proxies.append({
                "ip_port": f"{ip}:{port}",
                "auth": ""
            })
        else:  # Trường hợp có username và password
            username = parts[2]
            password = parts[3].replace('\r', '')  # Loại bỏ ký tự \r nếu có
            proxies.append({
                "ip_port": f"{ip}:{port}",
                "auth": f"{username}:{password}"
            })
    
    return proxies

def check_slot_goethe(url_with_cookies, html_data):
    """Kiểm tra slot và gửi tin nhắn nếu có slot"""
    # Phân tích HTML với BeautifulSoup
    soup = BeautifulSoup(html_data, 'html.parser')

    # Selector để tìm các phần tử phù hợp
    selector = "div.cs-input__field.cs-input__field--exams.cs-checkbox"
    elements = soup.select(selector)
    
    text = "Còn slot:"
    
    # Duyệt qua từng phần tử
    for element in elements:
        # Lấy nội dung của phần tử với class 'cs-checkbox__exam-type'
        text1 = element.select_one(".cs-checkbox__exam-type").get_text(strip=True).lower().replace("\n", " ").replace("\r", " ")
        # Lấy nội dung của phần tử với class 'cs-checkbox__exam-details'
        text2 = element.select_one(".cs-checkbox__exam-details").get_text(strip=True).lower().replace("\n", " ").replace("\r", " ")
        
        # Mảng các kỹ năng cần kiểm tra
        terms = [
            "đọc", "nghe", "viết", "nói",
            "reading", "listening", "writing", "speaking",
            "lesen", "hören", "schreiben", "sprechen"
        ]
        
        for term in terms:
            if not text2 and term in text1:
                text += f" {term}"
            if term in text1 and "chỗ trống" in text2:
                text += f" {term}"
    
    # Gộp các tin nhắn thành một tin nhắn duy nhất
    message = f"\n{url_with_cookies}\n{text.strip()}"
    send_telegram_message(message)

def check_url_register(api):
    urls = []
    file_path='proxy.txt'
    proxies = get_proxies(file_path)
    random_proxy = random.choice(proxies)
    proxy_url = f"http://{random_proxy['auth']}@{random_proxy['ip_port']}"
    
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(api, proxies={"http": proxy_url, "https": proxy_url})
        response.raise_for_status()
        body = response.json()
        # find url register
        urls = [
            f"https://www.goethe.de/coe/entry?lang=vi&oid={user['oid']}"
            for user in body['DATA']
            if not user.get('buttonDisabled', True)
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return urls