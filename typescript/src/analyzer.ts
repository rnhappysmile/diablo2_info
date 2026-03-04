import { areaDataRaw } from "./area";

// 상수 및 매핑 데이터
const IMM_MAP: Record<string, string> = {
  f: '화염', c: '냉기', l: '번개', p: '독', ph: '물리', m: '마법'
};

export const createAreaMap = (dataArray: any[]): Record<string, string> => {
  const mapping: Record<string, string> = {};

  // 배열의 첫 번째 요소인 거대 객체를 가져옴
  const data = dataArray[0];

  // 객체의 키(예: "Rogue_Encampment")를 순회
  Object.keys(data).forEach((key) => {
    const item = data[key];
    const enName = item["en-us"]; // en이 아니라 en-us입니다.
    const koName = item["ko"];

    if (enName && koName) {
      // 1. 기본 영문 이름 매핑
      mapping[enName] = koName;

      // 2. 공백을 언더바로 바꾼 이름 매핑 (예: "Rogue Encampment" -> "Rogue_Encampment")
      mapping[enName.replace(/ /g, "_")] = koName;

      // 3. 데이터 자체의 키값 매핑 (예: "Rogue_Encampment"도 이미 존재하므로 추가)
      mapping[key] = koName;
    }
  });

  return mapping;
};

const AREA_MAP = createAreaMap(areaDataRaw);

// 우버디아 상태 분석
export function analyzeDC(data: DiabloClone[]): string {
  const msgLines = ["[우버디아 서버 상태 알림]"];
  data.forEach(item => {
    if (item.state === 0 || item.region === "cn") return;

    const region = item.region.toUpperCase();
    const displayState = item.state + 1; // +1 로직 (0~5 -> 1~6)
    const mode = item.hardcore ? "하드코어" : "스탠다드";
    const ladder = item.ladder ? "래더" : "비래더";
    const dlc = item.dlc === "LoD" ? "확장팩" : "악마술사의 군림";

    msgLines.push(`[${region}] ${dlc} ${ladder} ${mode} (상태: ${displayState}/6)`);
  });
  return msgLines.length > 1 ? msgLines.join("\n") : "[우버디아] 현재 활성화된 전파 상태가 없습니다.";
}

// 테러존 분석
export function analyzeTZ(data: TerrorZone[]): string {
  if (!data || data.length < 2) return "테러존 정보가 부족합니다.";

  const formatEntry = (item: TerrorZone, title: string) => {
    const translatedZones = item.zone_name.map(zone => AREA_MAP[zone] || zone.replace(/_/g, " "));

    // 시간 변환 (KST 기준)
    const formatTime = (ts: number) => new Date(ts * 1000).toLocaleTimeString('ko-KR', {
      hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Seoul'
    });

    const timeStr = `${formatTime(item.time)} ~ ${formatTime(item.end_time)}`;
    const immunes = item.immunities.map(i => IMM_MAP[i] || i).join(", ") || "없음";

    return `[${title}]\n지역 : ${translatedZones.join(", ")}\n시간 : ${timeStr}\n등급 : 아이템(${item["tier-loot"]}), 경험치(${item["tier-exp"]})\n면역 : ${immunes}`;
  };

  return `${formatEntry(data[1], "현재 테러 존")}\n\n${formatEntry(data[0], "다음 예정 테러 존")}`;
}