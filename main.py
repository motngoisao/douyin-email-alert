import time
import requests
import smtplib
from email.mime.text import MIMEText

# Thông tin người nhận email
RECEIVER_EMAIL = "cutephamdao@gmail.com"

# Thông tin tài khoản Douyin cần theo dõi
DOUYIN_USER_URL = "https://www.douyin.com/user/MS4wLjABAAAA47XynWcbvp4Ds2RaAH5WUSveBLvGGammn8o3TpSLW39bPJ-tCRZKK--NvcXCTLXf"

# Thời gian kiểm tra lại sau mỗi lần (tính bằng giây)
CHECK_INTERVAL = 10

# Lưu video ID cuối cùng để kiểm tra
latest_video_id = None

def get_latest_video_id():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(DOUYIN_USER_URL, headers=headers)
    if response.status_code == 200:
        if "https://www.douyin.com/video/" in response.text:
            # Tìm video ID đầu tiên trong HTML
            start = response.text.find("https://www.douyin.com/video/")
            end = response.text.find('"', start)
            video_url = response.text[start:end]
            return video_url
    return None

def send_email_notification(video_url):
    msg = MIMEText(f"Tài khoản Douyin vừa đăng video mới: {video_url}")
    msg["Subject"] = "Thông báo Douyin mới"
    msg["From"] = RECEIVER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # Cấu hình SMTP cho Gmail
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(RECEIVER_EMAIL, "atio aqhh qvgh izvu")
        server.send_message(msg)
        server.quit()
        print("✅ Đã gửi email thông báo.")
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")

if __name__ == "__main__":
    print("🔍 Bắt đầu theo dõi tài khoản Douyin...")
    while True:
        try:
            current_video = get_latest_video_id()
            if current_video and current_video != latest_video_id:
                latest_video_id = current_video
                print(f"🎥 Video mới phát hiện: {current_video}")
                send_email_notification(current_video)
