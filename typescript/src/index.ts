import { initLogger, log } from './logger';
import { fetchGameData } from './api';
import { createAreaMap, analyzeDC, analyzeTZ } from './analyzer';
import { sendDiscordWebhooks } from './discord';

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
		try {
			log.info("실행 시작");
			log.info("API 동시 호출");
			
			const {tzData, dcData} = await fetchGameData(env);

			if (!tzData || !dcData) throw new Error("API 응답 데이터가 없습니다.");

			// 2. 데이터 가공
			log.info("데이터 가공 중...");
			const tzInfo = analyzeTZ(tzData);
			const dcInfo = analyzeDC(dcData);
			const finalMessage = `${tzInfo}\n\n${dcInfo}`;
			log.debug("tzInfo 내용: \n" + tzInfo);
			log.debug("tzInfo 내용: \n" + dcInfo);

			// 3. 디스코드 웹훅 전송
			await sendDiscordWebhooks(env, finalMessage);

			log.info("디스코드 웹훅 전송 완료");
			return finalMessage;
		} catch (error) {
			const errorMsg = `🚨 에러 발생: ${error instanceof Error ? error.message : String(error)}`;
			console.error(errorMsg);
			return errorMsg;
		}
	}
};