import { initLogger, log } from '../logger';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { sendDiscordWebhooks } from '../discord';

initLogger({ ENVIRONMENT: 'development' } as any);

describe('Discord 알림 전송 테스트', () => {
  beforeEach(() => {
    // 각 테스트 시작 전에 fetch 모킹 초기화
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
    });
  });

  it('여러 개의 웹훅 URL로 메시지를 각각 전송해야 한다', async () => {
    const env = {
      // 쉼표로 구분된 두 개의 가짜 웹훅 URL
      DISCORD_WEBHOOKS: 'https://webhook.one, https://webhook.two'
    };
    const tzInfo = '🔥 공포의 영역: 카우방';

    await sendDiscordWebhooks(env as any, tzInfo);

    // 1. 웹훅이 2번 호출되었는지 확인
    expect(global.fetch).toHaveBeenCalledTimes(2);

    // 2. 첫 번째 호출의 URL과 데이터가 맞는지 확인
    const [firstUrl, firstRequest] = vi.mocked(global.fetch).mock.calls[0];
    expect(firstUrl).toBe('https://webhook.one');
    
    // 3. 전송된 JSON 바디에 우리 메시지가 포함되어 있는지 확인
    const body = JSON.parse(firstRequest?.body as string);
    expect(body.content).toContain('공포의 영역');
    expect(body.content).toContain('카우방');
  });

  it('웹훅 URL 설정이 비어있어도 에러 없이 동작해야 한다', async () => {
    const env = { DISCORD_WEBHOOKS: '' };
    
    await expect(sendDiscordWebhooks(env as any, 'test'))
      .resolves.not.toThrow();
    
    expect(global.fetch).not.toHaveBeenCalled();
  });
});