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

def test_split_webhook_urls():
    if not WEBHOOK_URLS:
        print("설정된 웹훅 URL이 없습니다.")
        return
    
    try:
        for url in WEBHOOK_URLS:
            print(f"전송 결과({url})")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    test_split_webhook_urls()