import { initLogger, log } from '../logger';
import { describe, it, expect, vi } from 'vitest';
import { fetchGameData } from '../api';

initLogger({ ENVIRONMENT: 'development' } as any);

describe('API 호출 테스트', () => {
    it('API 호출 성공 시 데이터를 객체로 반환해야 한다', async () => {
        // 가짜 환경 변수
        const env = {
            TERROR_ZONE_API_URL: 'https://api.test/tz',
            DIABLO_CLONE_API_URL: 'https://api.test/dc',
            D2TZ_TOKEN: 'test-token'
        };

        // fetch를 가짜로 만듦
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: () => Promise.resolve([{ zone: 'Blood Moor' }])
        });

        const data = await fetchGameData(env);

        expect(data).toHaveProperty('tzData');
        expect(data).toHaveProperty('dcData');
        expect(global.fetch).toHaveBeenCalledTimes(2);
    });
});

describe('API 실패 호출 테스트', () => {
    it('API 서버가 500 에러를 응답하면 예외를 던져야 한다', async () => {
        // fetch가 실패 응답을 주는 상황을 가정
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            status: 500
        });

        const env = { TERROR_ZONE_API_URL: '...', D2TZ_TOKEN: '...' };

        // 에러가 발생하는지 검증
        await expect(fetchGameData(env)).rejects.toThrow("Terror Zone API 호출 실패");
    });
});