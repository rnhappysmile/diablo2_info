# tests/test_d2r.py
from src.main import diablo_clone_status
from src.main import terror_zone_status

def test_state_plus_one_logic():
    """state 값이 0이 아닐 때 +1 되어서 출력되는지 확인"""
    
    test_data = [{"region": "asia", "ladder": True, "hardcore": True, "dlc": "LoD", "state": 1}, 
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

    result = diablo_clone_status(test_data)
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

def test_terror_zone_status():
    # 복사해오신 데이터를 raw_json이나 리스트로 넣습니다.
    tz_data = [
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
    
    result = terror_zone_status(tz_data)
    
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