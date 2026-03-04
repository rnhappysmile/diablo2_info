import requests
import os
import json
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 1. 현재 파일의 위치를 기준으로 ../configs/.env 경로 계산
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".." / "configs" / ".env"

# .env 파일이 있으면 로드합니다 (로컬 환경용)
# GitHub Actions 환경에서는 .env가 없으므로 무시되고 시스템 환경 변수(Secrets)를 읽습니다.
load_dotenv(dotenv_path=env_path)

# 환경 변수에서 URL을 가져옵니다.
# 로컬 .env에 값이 있으면 그 값을, 없으면 GitHub Secrets 값을 가져오게 됩니다.
webhook_raw = os.getenv("DISCORD_WEBHOOKS", "")
D2TZ_TOKEN = os.getenv("D2TZ_TOKEN", "")
TERROR_ZONE_API_URL = os.getenv("TERROR_ZONE_API_URL", "https://api.d2tz.info/public/tz?token=")
DIABLO_CLONE_API_URL = os.getenv("DIABLO_CLONE_API_URL", "https://api.d2tz.info/public/dc?token=")
WEBHOOK_URLS = [url.strip() for url in webhook_raw.split(",") if url.strip()]

# 유효한 URL만 필터링
WEBHOOK_URLS = [url for url in WEBHOOK_URLS if url]

def load_area_mapping():
    """area.json 파일을 읽어서 영어:한글 매핑 딕셔너리를 반환"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "..", "data", "area.json")
        abs_path = os.path.normpath(file_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            area_data = json.load(f)
        
        # area.json 구조가 [{"en": "Outer Steppes", "ko": "외부 평원"}, ...] 형태일 경우
        # 혹은 {"Outer_Steppes": "외부 평원"} 형태일 경우에 맞춰 매핑 생성
        # d2tz 데이터 특성상 영어 이름을 키로, ko 값을 밸류로 만듭니다.
        mapping = {}
        if isinstance(area_data, list):
            for item in area_data:
                if isinstance(item, dict):
                    en = item.get("en")
                    ko = item.get("ko")
                    if en and ko:
                        mapping[en] = ko
                        mapping[en.replace(" ", "_")] = ko
        elif isinstance(area_data, dict):
            # 만약 {"English Name": "한글 이름"} 형태라면
            for en, ko in area_data.items():
                mapping[en] = ko
                mapping[en.replace(" ", "_")] = ko
        return mapping
    except FileNotFoundError:
        print("경고: area.json 파일을 찾을 수 없습니다. 영어 이름이 그대로 표시됩니다.")
        return {}

# 전역 변수로 매핑 데이터를 한 번 로드해둡니다.
AREA_MAP = load_area_mapping()

# 30분 마다 우버디아 체크하는게 의미가 있을까? 혹시 모름을 위해 1이 아닌 경우만 안내할까 
def diablo_clone_status(data):
    issues = [item for item in data]
    
    msg_lines = ["[우버디아 서버 상태 알림]"]
    
    for item in issues:
        if item['state'] == 0 or item['region'] == "cn":
            continue

        region = item['region'].upper()
        # +1 로직 적용 (0~5 -> 1~6)
        display_state = item['state'] + 1
        
        # 가독성을 위한 이모지 분기 (필요에 따라 수정)
        #emoji = "⚠️" if display_state <= 3 else "🚫"
        
        mode = "하드코어" if item['hardcore'] else "스탠다드"
        ladder = "래더" if item['ladder'] else "비래더"
        dlc = "확장팩" if item['dlc'] == "LoD" else "악마술사의 군림"
        
        #msg_lines.append(f"{emoji} [{region}] {dlc} {ladder} {mode} (상태: {display_state})")
        msg_lines.append(f"[{region}] {dlc} {ladder} {mode} (상태: {display_state}/6)")

    return "\n".join(msg_lines)

def analyze_tz(terror_zone_data):
    if not terror_zone_data or len(terror_zone_data) < 2:
        return "테러존 정보가 부족합니다."

    # 면역 약어를 한글로 바꾸는 공통 매핑 테이블
    imm_map = {'f': '화염', 'c': '냉기', 'l': '번개', 'p': '독', 'ph': '물리', 'm': '마법'}

    def format_entry(item, title):
        # 지역명 한글 변환 로직
        translated_zones = []
        for zone in item['zone_name']:
            # area.json에 매핑된 한글 이름이 있으면 쓰고, 없으면 언더바만 제거해서 표시
            ko_zone = AREA_MAP.get(zone, zone.replace("_", " "))
            translated_zones.append(ko_zone.get('ko', zone.replace("_", " ")))
        
        zones_text = ", ".join(translated_zones)
        
        # 시간 변환
        start_dt = datetime.fromtimestamp(item['time'])
        end_dt = datetime.fromtimestamp(item['end_time'])
        time_str = f"{start_dt.strftime('%H:%M')} ~ {end_dt.strftime('%H:%M')}"
        
        # 면역 가공
        translated_imm = [imm_map.get(i, i) for i in item.get('immunities', [])]
        imm_text = ", ".join(translated_imm) if translated_imm else "없음"
        
        # 한 덩어리의 메시지 생성
        return (
            f"[{title}]\n"
            f"지역 : {zones_text}\n"
            f"시간 : {time_str}\n"
            f"등급 : 아이템({item.get('tier-loot', 'N/A')}), 경험치({item.get('tier-exp', 'N/A')})\n"
            f"면역 : {imm_text}"
        )

    # 현재(data[0])와 다음(data[1]) 데이터를 각각 포맷팅
    current_msg = format_entry(terror_zone_data[1], "현재 테러 존")
    next_msg = format_entry(terror_zone_data[0], "다음 예정 테러 존")

    return f"{current_msg}\n\n{next_msg}"

    assert "대박" in result

def fetch_d2tz_data(api_url):
    """API로부터 데이터를 요청하여 JSON으로 반환"""
    try:
        response = requests.get(api_url)
        response.raise_for_status() # 200 OK가 아니면 에러 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패 ({api_url}): {e}")
        return None
    
def get_terror_zone_info():
    """테러 존 정보를 가져와서 포맷팅"""
    data = fetch_d2tz_data(f"{TERROR_ZONE_API_URL}{D2TZ_TOKEN}")
    if not data:
        return "테러 존 정보를 가져올 수 없습니다."
    
    # 이전에 작성한 analyze_tz 함수를 호출하여 문자열 생성
    return analyze_tz(data)

def get_diablo_clone_info():
    """디아블로 복제(우버디아) 상태 정보를 가져와서 포맷팅"""
    data = fetch_d2tz_data(f"{DIABLO_CLONE_API_URL}{D2TZ_TOKEN}")
    if not data:
        return "디아블로 복제 정보를 가져올 수 없습니다."

    # 예시: 데이터 구조에 따른 간단한 포맷팅 (실제 응답 구조에 맞춰 조정 필요)
    results = diablo_clone_status(data)
    
    return results

def send_webhook(message):
    if not WEBHOOK_URLS:
        print("설정된 웹훅 URL이 없습니다.")
        return
    
    payload = {'content': f"{message}\n\nData courtesy of [d2tz.info](<https://www.d2tz.info/>)"}

    try:
        for url in WEBHOOK_URLS:            
            res = requests.post(url, data=payload)
            print(f"전송 결과({url}): {res.status_code}")

    except Exception as e:
        print(f"에러 발생: {e}")

def diablo_info():
    """우버디아 상태와 테러존 정보를 가져와서 출력"""
    tz_info = get_terror_zone_info()
    d2tz_info = get_diablo_clone_info()
    
    #print("tz_info:", tz_info)
    #print("d2tz_info:", d2tz_info)

    message = f"{tz_info}\n\n{d2tz_info}"  
    #print(message)
    
    return message

def run():
    #d2tz에서 데이터 받아오기
    print("실행 시작")
    message = diablo_info()
    send_webhook(message)

if __name__ == "__main__":
    run()