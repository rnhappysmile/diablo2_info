// tests/setup.ts
import { initLogger } from '../logger';

// 모든 테스트 실행 전 로거 초기화
initLogger({ ENVIRONMENT: 'development' } as any);