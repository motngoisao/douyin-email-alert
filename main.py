import time
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Cấu hình
DOUYIN_USER_URL = "https://www.douyin.com/user/MS4wLjABAAAA47XynWcbvp4Ds2RaAH5WUSveBLvGGammn8o3TpSLW39bPJ-tCRZKK--NvcXCTLXf"
CHECK_INTERVAL = 10  # kiểm tra mỗi 10 giây

# Cấu hình email
EMAIL_SENDER = 'cutephamdao@gmail.com'
EMAIL_PASSWORD = 'atio aqhh qvgh izvu'
EMAIL_RECEIVER = 'cutephamdao@gmail.com'

last_video_id = None

def get_latest_video_id():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(DOUYIN_USER_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            if '/video/' in a['href']:
                video_id = a['href'].split('/video/')[1].split('?')[0]
                return video_id
    except Exception as e:
        print(f"Lỗi khi lấy video: {e}")
    return None

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Đã gửi email!")
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")

if __name__ == "__main__":
    print("🚀 Đang theo dõi tài khoản Douyin...")
    while True:
        video_id = get_latest_video_id()
        if video_id and video_id != last_video_id:
            print(f"🎉 Phát hiện video mới: {video_id}")
            last_video_id = video_id
            video_link = f"https://www.douyin.com/video/{video_id}"
            send_email("📢 Douyin có video mới!", f"Xem tại đây: {video_link}")
        else:
            print("⏳ Không có video mới...")
        time.sleep(CHECK_INTERVAL)
