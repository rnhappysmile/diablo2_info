import requests
import os
from io import BytesIO
from dotenv import load_dotenv

# .env 파일이 있으면 로드합니다 (로컬 환경용)
# GitHub Actions 환경에서는 .env가 없으므로 무시되고 시스템 환경 변수(Secrets)를 읽습니다.
load_dotenv()

# 환경 변수에서 URL을 가져옵니다.
# 로컬 .env에 값이 있으면 그 값을, 없으면 GitHub Secrets 값을 가져오게 됩니다.
WEBHOOK_URLS = [
    os.getenv('WEBHOOK_URL_1'),
    os.getenv('WEBHOOK_URL_2')
]

# 유효한 URL만 필터링
WEBHOOK_URLS = [url for url in WEBHOOK_URLS if url]

def send_webhook():
    if not WEBHOOK_URLS:
        print("설정된 웹훅 URL이 없습니다.")
        return

    IMAGE_URL = "https://api.d2tz.info/public/tz_image?l=ko"
    
    try:
        response = requests.get(IMAGE_URL)
        response.raise_for_status()
        image_data = response.content

        for i, url in enumerate(WEBHOOK_URLS, 1):
            image_file = BytesIO(image_data)
            files = {'file': ('tz_image.png', image_file, 'image/png')}
            payload = {'content': "Data courtesy of [d2tz.info](<https://www.d2tz.info/>)"}
            
            res = requests.post(url, data=payload, files=files)
            print(f"전송 결과({i}): {res.status_code}")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    send_webhook()