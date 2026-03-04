import requests
import os
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv

# 1. 현재 파일의 위치를 기준으로 ../configs/.env 경로 계산
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".." / "configs" / ".env"

# .env 파일이 있으면 로드합니다 (로컬 환경용)
# GitHub Actions 환경에서는 .env가 없으므로 무시되고 시스템 환경 변수(Secrets)를 읽습니다.
load_dotenv(dotenv_path=env_path)

# 환경 변수에서 URL을 가져옵니다.
# 로컬 .env에 값이 있으면 그 값을, 없으면 GitHub Secrets 값을 가져오게 됩니다.
webhook_raw = os.getenv("DISCORD_WEBHOOKS", "")
WEBHOOK_URLS = [url.strip() for url in webhook_raw.split(",") if url.strip()]

# 유효한 URL만 필터링
WEBHOOK_URLS = [url for url in WEBHOOK_URLS if url]

# 30분 마다 우버디아 체크하는게 의미가 있을까? 혹시 모름을 위해 1이 아닌 경우만 안내할까 
def diablo_clone_status(data):
    issues = [item for item in data]
    
    msg_lines = ["우버디아 서버 상태 알림"]
    
    for item in issues:
        if item['state'] == 0:
            continue

        region = item['region'].upper()
        # +1 로직 적용 (0~5 -> 1~6)
        display_state = item['state'] + 1
        
        # 가독성을 위한 이모지 분기 (필요에 따라 수정)
        #emoji = "⚠️" if display_state <= 3 else "🚫"
        
        mode = "하드코어" if item['hardcore'] else "스탠다드"
        ladder = "래더" if item['ladder'] else "비래더"
        dlc = "확장팩" if item['dlc'] == "LoD" else "오리지널"
        
        #msg_lines.append(f"{emoji} [{region}] {dlc} {ladder} {mode} (상태: {display_state})")
        msg_lines.append(f"[{region}] {dlc} {ladder} {mode} (상태: {display_state})")

    return "\n".join(msg_lines)

def send_webhook():
    if not WEBHOOK_URLS:
        print("설정된 웹훅 URL이 없습니다.")
        return

    IMAGE_URL = "https://api.d2tz.info/public/tz_image?l=ko"
    
    try:
        response = requests.get(IMAGE_URL)
        response.raise_for_status()
        image_data = response.content

        for url in WEBHOOK_URLS:
            image_file = BytesIO(image_data)
            files = {'file': ('tz_image.png', image_file, 'image/png')}
            payload = {'content': "Data courtesy of [d2tz.info](<https://www.d2tz.info/>)"}
            
            res = requests.post(url, data=payload, files=files)
            print(f"전송 결과({url}): {res.status_code}")

    except Exception as e:
        print(f"에러 발생: {e}")

def run():
    send_webhook()

if __name__ == "__main__":
    run()