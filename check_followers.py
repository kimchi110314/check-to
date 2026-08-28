import json
import os
import smtplib
import sys
from email.mime.text import MIMEText

import requests

# ===== 설정 =====
CHANNEL_ID = "2708947b66f527fd74e6b3d6bcc1349b"  # 러끼 채널 ID
TARGET_FOLLOWERS = 100_000
STATE_FILE = "state.json"

CHZZK_API_URL = f"https://api.chzzk.naver.com/service/v1/channels/{CHANNEL_ID}"


def get_follower_count() -> int:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(CHZZK_API_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["content"]["followerCount"]


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_count": None, "notified": False}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["NOTIFY_EMAIL"]

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, [recipient], msg.as_string())


def main() -> None:
    count = get_follower_count()
    print(f"현재 팔로워 수: {count:,}명")

    state = load_state()
    state["last_count"] = count

    if count >= TARGET_FOLLOWERS and not state.get("notified"):
        subject = "🎉 러끼 팔로워 10만 명 달성!"
        body = f"러끼 채널의 팔로워 수가 {count:,}명이 되어 10만 명을 달성했습니다!"
        send_email(subject, body)
        state["notified"] = True
        print("알림 메일 발송 완료")
    else:
        print("아직 조건 미달성이거나 이미 알림을 보냈습니다.")

    save_state(state)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"오류 발생: {e}", file=sys.stderr)
        sys.exit(1)
