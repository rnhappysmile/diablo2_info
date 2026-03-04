// src/api.ts
import { log } from './logger';

export async function fetchGameData(env: any) {
    const { TERROR_ZONE_API_URL, DIABLO_CLONE_API_URL, D2TZ_TOKEN } = env;

    log.info("API 동시 호출 시작...");

    // Promise.all을 사용해 두 API를 병렬로 호출 (시간 단축)
    const [tzRes, dcRes] = await Promise.all([
        fetch(`${TERROR_ZONE_API_URL}${D2TZ_TOKEN}`),
        fetch(`${DIABLO_CLONE_API_URL}${D2TZ_TOKEN}`)
    ]);

    // 응답 상태 확인
    if (!tzRes.ok) {
        log.error(`Terror Zone API 오류: ${tzRes.status}`);
        throw new Error("Terror Zone API 호출 실패");
    }
    if (!dcRes.ok) {
        log.error(`Diablo Clone API 오류: ${dcRes.status}`);
        throw new Error("Diablo Clone API 호출 실패");
    }

    // JSON 파싱
    const tzData = await tzRes.json() as TerrorZone[];
    const dcData = await dcRes.json() as DiabloClone[];

    log.info("API 데이터 수신 완료");

    return { tzData, dcData };
}