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

interface AreaMapping {
    en: string;
    ko: string;
}

interface Env {
	D2TZ_TOKEN: string;
	TERROR_ZONE_API_URL: string;
	DIABLO_CLONE_API_URL: string;
	DISCORD_WEBHOOKS: string;
	ENVIRONMENT: string;
}