// types.ts (또는 index.ts 상단)
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