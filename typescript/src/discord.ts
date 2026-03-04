import { log } from './logger';

export async function sendDiscordWebhooks(env: Env, message: string) {
    const webhookUrls = env.DISCORD_WEBHOOKS.split(",").map(u => u.trim()).filter(Boolean);
    const payload = {
        content: `${message}\n\nData courtesy of [d2tz.info](<https://www.d2tz.info/>)`
    };

    log.info(`웹훅 전송 시작 (${webhookUrls.length}곳)`);

    await Promise.all(webhookUrls.map(url =>
        fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
    ));
}