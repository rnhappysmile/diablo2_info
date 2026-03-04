import { areaDataRaw } from "./area";
import { initLogger, log } from './logger';

// --- 1. 타입 정의 (Interfaces) ---
interface TerrorZone {
  time: number;
  end_time: number;
  zone_name: string[];
  "tier-loot": string;
  "tier-exp": string;
  immunities: string[];
}

interface DiabloClone {
  region: string;
  state: number;
  hardcore: boolean;
  ladder: boolean;
  dlc: string;
}

interface Env {
  D2TZ_TOKEN: string;
  TERROR_ZONE_API_URL: string;
  DIABLO_CLONE_API_URL: string;
  DISCORD_WEBHOOKS: string;
  ENVIRONMENT: string;
}

// --- 2. 매핑 데이터 생성 ---
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

// --- 3. 가공 로직 (Logic Functions) ---

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

// --- 4. 메인 핸들러 (Main Handler) ---

export default {
  // 스케줄러 트리거 (Cron)
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
	initLogger(env); // 2. 여기서 활성화!
	ctx.waitUntil(this.run(env));
  },

  // HTTP 트리거 (웹 접속 테스트용)
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
	initLogger(env); // 2. 여기서 활성화!
	const url = new URL(request.url);

    // 1. 파비콘 요청은 그냥 무시하고 404를 돌려줌
    if (url.pathname === '/favicon.ico') {
      return new Response(null, { status: 404 });
    }

	const message = await this.run(env);
    return new Response(message || "실행 완료 (메시지 없음)", { status: 200 });
  },

  // 공통 실행 로직
  async run(env: Env): Promise<string> {
    const { D2TZ_TOKEN, TERROR_ZONE_API_URL, DIABLO_CLONE_API_URL, DISCORD_WEBHOOKS, ENVIRONMENT } = env;

    try {
		log.info("실행 시작");
		log.info("API 동시 호출");
	  // 1. API 동시 호출
      const [tzRes, dcRes] = await Promise.all([
        fetch(`${TERROR_ZONE_API_URL}${D2TZ_TOKEN}`),
        fetch(`${DIABLO_CLONE_API_URL}${D2TZ_TOKEN}`)
      ]);
	  log.debug("TERROR_ZONE_API_URL 확인: ", TERROR_ZONE_API_URL);
      log.debug("DIABLO_CLONE_API_URL 확인: ", DIABLO_CLONE_API_URL);
      log.debug("ENVIRONMENT 확인: ", ENVIRONMENT);

      if (!tzRes.ok || !dcRes.ok) throw new Error("API 응답 상태가 좋지 않습니다.");

      const tzData = await tzRes.json() as TerrorZone[];
      const dcData = await dcRes.json() as DiabloClone[];

      // 2. 데이터 가공
	  log.info("데이터 가공 중...");
      const tzInfo = analyzeTZ(tzData);
      const dcInfo = analyzeDC(dcData);
      const finalMessage = `${tzInfo}\n\n${dcInfo}`;
	  log.debug("tzInfo 내용: \n" + tzInfo);
	  log.debug("tzInfo 내용: \n" + dcInfo);

      // 3. 디스코드 웹훅 전송
	  log.info("디스코드 웹훅 전송 준비");
	  log.debug("메시지 내용: \n" + finalMessage);
      const webhookUrls = DISCORD_WEBHOOKS.split(",").map(url => url.trim()).filter(url => url);
      const payload = {
        content: `${finalMessage}\n\nData courtesy of [d2tz.info](<https://www.d2tz.info/>)`
      };

      await Promise.all(webhookUrls.map(url => 
        fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        })
      ));

      log.info("디스코드 웹훅 전송 완료");
      return finalMessage;
    } catch (error) {
      const errorMsg = `🚨 에러 발생: ${error instanceof Error ? error.message : String(error)}`;
      console.error(errorMsg);
      return errorMsg;
    }
  }
};