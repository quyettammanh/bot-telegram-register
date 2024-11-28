# cronjob.py

import time
import subprocess

def run_main():
    try:
        # Gọi script main.py
        result = subprocess.run(["python", "./main.py"], check=True, capture_output=True, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def start_cronjob():
    while True:
        run_main()  # Chạy main.py
        print("Waiting for next minute...")
        time.sleep(60)  # Đợi 60 giây (1 phút) trước khi chạy lại

if __name__ == "__main__":
    start_cronjob()  # Bắt đầu cronjob
