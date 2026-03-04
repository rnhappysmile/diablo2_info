// 상수 및 매핑 데이터
const IMM_MAP: Record<string, string> = {
  f: '화염', c: '냉기', l: '번개', p: '독', ph: '물리', m: '마법'
};

// 1. 테러존 분석 함수
function analyzeTZ(data: TerrorZone[], areaMap: Record<string, string>): string {
  if (!data || data.length < 2) return "테러존 정보가 부족합니다.";

  const formatEntry = (item: TerrorZone, title: string) => {
    const translatedZones = item.zone_name.map(zone => {
      // area.json 매핑 확인 (언더바 제거 로직 포함)
      return areaMap[zone] || areaMap[zone.replace(/ /g, "_")] || zone.replace(/_/g, " ");
    });

    const startTime = new Date(item.time * 1000).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
    const endTime = new Date(item.end_time * 1000).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
    
    const immunes = item.immunities.map(i => IMM_MAP[i] || i).join(", ") || "없음";

    return `[${title}]\n지역 : ${translatedZones.join(", ")}\n시간 : ${startTime} ~ ${endTime}\n등급 : 아이템(${item["tier-loot"]}), 경험치(${item["tier-exp"]})\n면역 : ${immunes}`;
  };

  return `${formatEntry(data[1], "현재 테러 존")}\n\n${formatEntry(data[0], "다음 예정 테러 존")}`;
}

// 2. 우버디아 상태 분석 함수
function analyzeDC(data: DiabloClone[]): string {
  const msgLines = ["[우버디아 서버 상태 알림]"];
  
  data.forEach(item => {
    if (item.state === 0 || item.region === "cn") return;

    const region = item.region.toUpperCase();
    const displayState = item.state + 1;
    const mode = item.hardcore ? "하드코어" : "스탠다드";
    const ladder = item.ladder ? "래더" : "비래더";
    const dlc = item.dlc === "LoD" ? "확장팩" : "오리지널";

    msgLines.push(`[${region}] ${dlc} ${ladder} ${mode} (상태: ${displayState}/6)`);
  });

  return msgLines.join("\n");
}