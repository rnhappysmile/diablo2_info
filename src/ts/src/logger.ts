export interface Env {
    ENVIRONMENT: string;
}

// 로거의 실제 기능을 담을 변수 (처음엔 비어있음)
let loggerInstance: {
    info: (msg: string) => void;
    debug: (msg: string, data?: any) => void;
    error: (msg: string, err?: any) => void;
} | null = null;

// 1. 워커 시작 시 딱 한 번만 호출해서 로거를 활성화하는 함수
export const initLogger = (env: Env) => {
    if (loggerInstance) return; // 이미 초기화됐다면 무시

    const isDev = env.ENVIRONMENT === 'development';

    loggerInstance = {
        info: (msg) => console.info(`[INFO] ${msg}`),
        debug: (msg, data) => {
            if (isDev) console.debug(`[DEBUG] ${msg}`, data);
        },
        error: (msg, err) => console.error(`[ERROR] ${msg}`, err),
    };
};

// 2. 다른 파일에서 import 해서 쓸 실제 로거 객체
export const log = {
    info: (msg: string) => loggerInstance?.info(msg),
    debug: (msg: string, data?: any) => loggerInstance?.debug(msg, data),
    error: (msg: string, err?: any) => loggerInstance?.error(msg, err),
};