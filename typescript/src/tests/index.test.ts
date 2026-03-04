import { describe, it, expect } from 'vitest';
// 테스트하고 싶은 함수들을 index.ts에서 export 해야 합니다.
import { createAreaMap, analyzeDC, analyzeTZ } from '../analyzer';

describe('우버디아(Diablo Clone) 분석 테스트', () => {

    it('우버디아 상태가 5에서 6로 정상 변환되는지 확인', () => {
        const mockData = [{
            region: "us",
            state: 5, // 파이썬 로직에 따라 5+1 = 1이 되어야 함
            hardcore: false,
            ladder: true,
            dlc: "LoD"
        }];

        const result = analyzeDC(mockData);
        debugLog("우버디아 상태 분석 결과", result);
        expect(result).toContain("(상태: 6/6)");
        expect(result).toContain("[US]");
    });
});

describe('테러존(Terror Zone) 분석 테스트', () => {
    it('테러존 지역명이 한글로 잘 매핑되는지 확인', () => {
        // AREA_MAP에 "Outer_Steppes"가 "핏빛 황무지"로 등록되어 있다고 가정
        const mockTZ = [{
            time: 1772652600,
            end_time: 1772654400,
            zone_name: ["Outer_Steppes", "Plains_of_Despair"],
            "tier-loot": "A",
            "tier-exp": "S",
            immunities: ["f", "c"]
        }, {
            time: 1772650800,
            end_time: 1772652600,
            zone_name: ["Tal_Rashas_Tomb", "Duriels_Lair", "Canyon_of_The_Magi"],
            "tier-loot": "B",
            "tier-exp": "A",
            immunities: ["l"]
        }];

        const result = analyzeTZ(mockTZ);
        debugLog("테러존 분석 결과", result);
        expect(result).toContain("평원 외곽");
        // AREA_MAP이 정상 작동한다면 한글 이름이 포함되어야 함
        // 만약 매핑 안 되면 "Cold Plains"처럼 출력될 것
    });
});

describe('지역 데이터 매핑 테스트', () => {
    it('지역 데이터가 한글로 잘 매핑되는지 확인', () => {
        // 간단한 테스트 코드
        const testData = [
            { en: "Cold Plains", ko: "차가운 평원" },
            { en: "Stony Field", ko: "바위 벌판" }
        ];

        const result = createAreaMap(testData);

        // 확인용 출력
        console.assert(result["Cold Plains"] === "차가운 평원", "기본 매핑 실패");
        console.assert(result["Cold_Plains"] === "차가운 평원", "언더바 치환 매핑 실패");

        if (result["Cold_Plains"] === "차가운 평원") {
            console.log("✅ 매핑 로직이 정상입니다!");
        }
    });
});

/**
 * 데이터를 터미널에 보기 좋게 출력하는 공통 함수
 * @param title 로그의 제목
 * @param data 출력할 데이터 (문자열, 객체, 배열 등 모두 가능)
 */
export function debugLog(title: string, data: any): void {
    const divider = "================================================";
    const timestamp = new Date().toLocaleString('ko-KR');

    console.log(`\n${divider}`);
    console.log(`[${timestamp}] 🚀 ${title}`);
    console.log(divider);

    if (typeof data === 'object') {
        // 객체나 배열은 JSON 형태로 예쁘게 출력
        console.log(JSON.stringify(data, null, 2));
    } else {
        // 문자열이나 숫자는 그대로 출력
        console.log(data);
    }

    console.log(`${divider}\n`);
}