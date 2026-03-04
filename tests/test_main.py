# tests/test_d2r.py
from unittest.mock import patch, MagicMock
from src.main import diablo_clone_status
from src.main import analyze_tz
from src.main import get_terror_zone_info, get_diablo_clone_info

DIABLO_CLONE_DATA = [{"region": "asia", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 1}, 
                 {"region": "asia", "ladder": True, "hardcore": False, "dlc": "LoD", "state": 3}, 
                 {"region": "asia", "ladder": False, "hardcore": True, "dlc": "LoD", "state": 1}, 
                 {"region": "asia", "ladder": False, "hardcore": False, "dlc": "LoD", "state": 3}, 
                 {"region": "asia", "ladder": True, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "asia", "ladder": True, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "asia", "ladder": False, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "asia", "ladder": False, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "eu", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 0}, 
                 {"region": "eu", "ladder": True, "hardcore": False, "dlc": "LoD", "state": 0}, 
                 {"region": "eu", "ladder": False, "hardcore": True, "dlc": "LoD", "state": 1}, 
                 {"region": "eu", "ladder": False, "hardcore": False, "dlc": "LoD", "state": 0}, 
                 {"region": "eu", "ladder": True, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "eu", "ladder": True, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "eu", "ladder": False, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "eu", "ladder": False, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "us", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 0}, 
                 {"region": "us", "ladder": True, "hardcore": False, "dlc": "LoD", "state": 0}, 
                 {"region": "us", "ladder": False, "hardcore": True, "dlc": "LoD", "state": 0}, 
                 {"region": "us", "ladder": False, "hardcore": False, "dlc": "LoD", "state": 0}, 
                 {"region": "us", "ladder": True, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "us", "ladder": True, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "us", "ladder": False, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "us", "ladder": False, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "cn", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 0}, 
                 {"region": "cn", "ladder": True, "hardcore": False, "dlc": "LoD", "state": 1}, 
                 {"region": "cn", "ladder": False, "hardcore": True, "dlc": "LoD", "state": 0}, 
                 {"region": "cn", "ladder": False, "hardcore": False, "dlc": "LoD", "state": 3}, 
                 {"region": "cn", "ladder": True, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "cn", "ladder": True, "hardcore": False, "dlc": "RotW", "state": 0}, 
                 {"region": "cn", "ladder": False, "hardcore": True, "dlc": "RotW", "state": 0}, 
                 {"region": "cn", "ladder": False, "hardcore": False, "dlc": "RotW", "state": 0}]

TZ_DATA = [
        {
            "time": 1772602200, 
            "zone_name": ["Outer_Steppes", "Plains_of_Despair"], 
            "immunities": ["f", "c", "l", "p", "ph", "m"],
            "tier-exp": "C", 
            "tier-loot": "C", 
            "area_id": 104, 
            "area_ids": [104, 105], 
            "end_time": 1772604000
        },
        {
            "time": 1772600400, 
            "zone_name": ["Tal_Rashas_Tomb", "Duriels_Lair", "Canyon_of_The_Magi"], 
            "immunities": ["f", "c", "l", "p", "ph", "m"], 
            "tier-exp": "S", 
            "tier-loot": "A", 
            "area_id": 46, 
            "area_ids": [46, 66, 67, 68, 69, 70, 71, 72, 73], 
            "end_time": 1772602200
        }
    ]

def test_state_plus_one_logic():
    """state 값이 0이 아닐 때 +1 되어서 출력되는지 확인"""


    result = diablo_clone_status(DIABLO_CLONE_DATA)
    print(result)  # 결과 출력하여 확인

# 1. 줄바꿈으로 쪼개고, 앞뒤 공백 제거 및 빈 줄 제외
    all_lines = [line.strip() for line in result.split('\n') if line.strip()]
    
    # 2. 제목 줄을 제외한 실제 데이터 줄만 추출
    # 방법 A: 첫 줄이 제목인 것을 알 경우 슬라이싱 사용
    data_lines = all_lines[1:] 
    
    # 3. 개수 검증 (정확히 7개여야 함)
    assert len(data_lines) == 7, f"데이터 개수 불일치: 기대값 7, 실제값 {len(data_lines)}"
    
    # 4. 제목 내용 검증 (선택 사항)
    assert "우버디아 서버 상태 알림" in all_lines[0]
    
    # 5. 특정 데이터 변환 확인 (상태 값이 잘 더해졌는지)
    # 예: ASIA 확장팩 래더 하드코어의 state는 1이었으므로 (상태: 2)가 포함되어야 함
    assert "[ASIA] 확장팩 래더 하드코어 (상태: 2)" in data_lines
    
    print(f"\n테스트 통과: 제목과 {len(data_lines)}개의 데이터 확인 완료!")

def test_state_boundary_logic():
    """경계값인 5가 들어왔을 때 6이 되는지 확인"""
    boundary_data = [{"region": "us", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 5}]
    result = diablo_clone_status(boundary_data)
    
    assert "(상태: 6)" in result

def test_analyze_tz():
    # 복사해오신 데이터를 raw_json이나 리스트로 넣습니다.   
    result = analyze_tz(TZ_DATA)
    
    print(f"\n{result}")  # 결과 출력하여 확인

    # 현재와 다음이라는 제목이 모두 있는지 확인
    assert "[현재 테러 존]" in result
    assert "[다음 예정 테러 존]" in result

    # 현재 테러존의 등급이 C로 표시되는지 확인
    assert "등급 : 아이템(A), 경험치(S)" in result
    
    # 다음 테러존 지역이 포함되었는지 확인
    assert "지역 : 평원 외곽, 절망의 평원" in result
    
    # 유지 시간이 연속되는지 확인 (예: 14:30가 양쪽에 있는지)
    assert result.count("14:30") >= 2

# 1. 테러 존 API 테스트
@patch('src.main.requests.get')
def test_get_terror_zone_info_success(mock_get):
    # 가짜 응답 데이터 설정
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = TZ_DATA
    mock_get.return_value = mock_response

    result = get_terror_zone_info()

    # 현재와 다음이라는 제목이 모두 있는지 확인
    assert "Outer_Steppes" in result
    assert "Tal_Rashas_Tomb" in result

    # 현재 테러존의 등급이 C로 표시되는지 확인
    assert "C" in result
    
    # 다음 테러존 지역이 포함되었는지 확인
    assert "1772600400" in result
    
    # 유지 시간이 연속되는지 확인 (예: 14:30가 양쪽에 있는지)
    assert result.count("14:30") >= 2

# 2. 우버디아(Diablo Clone) API 테스트
@patch('src.main.requests.get')
def test_get_diablo_clone_info_success(mock_get):
    # 가짜 응답 데이터 설정
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = DIABLO_CLONE_DATA
    mock_get.return_value = mock_response

    result = get_diablo_clone_info()

    # 검증: 각 지역별 진행도가 잘 표시되는지
    assert "asia" in result
    assert "RotW" in result
    assert "0" in result

# 3. API 요청 실패 시 테스트
@patch('src.main.requests.get')
def test_api_fetch_failure(mock_get):
    # 404 에러 시뮬레이션
    mock_get.side_effect = Exception("Connection Error")

    result_tz = get_terror_zone_info()
    result_dc = get_diablo_clone_info()

    assert "가져올 수 없습니다" in result_tz
    assert "가져올 수 없습니다" in result_dc