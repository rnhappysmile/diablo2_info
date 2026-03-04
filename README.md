# Diablo 2 Resurrected Info Bot
  A Diablo 2 Resurrected Information Notifier built on Cloudflare Workers. 
  It tracks data for Terror Zones (TZ) and Diablo Clone (DC) progress and sends updates via Discord Webhooks.


# Key Features
  - Terror Zone (TZ) Tracking: Fetches active Terror Zone data and translates area names into Korean.
  - Diablo Clone (DC) Monitoring: Monitors progression stages (1–6) and sends alerts upon status changes.
  - Discord Notifications: Supports multiple webhook URLs for simultaneous updates across various channels.
  - Lightweight & High Performance: Operates serverless within the Cloudflare Workers (TypeScript) environment.


# Tech Stack
  - Language: TypeScript
  - Runtime: Cloudflare Workers (Edge Computing)
  - Framework: Vitest (Unit Testing)
  - Deployment: Wrangler (Cloudflare CLI)


# Project Structure 
```
.
├── src/
│   ├── index.ts        # Worker Entry Point (Scheduled Event)
│   ├── api.ts          # External API Communication Logic
│   ├── analyzer.ts     # Data Analysis & Korean Translation Logic
│   ├── discord.ts      # Discord Webhook Transmission Logic
│   ├── logger.ts       # Global Logging System
│   └── types.ts        # TypeScript Interface Definitions
├── tests/              # Vitest Unit Test Suites
├── wrangler.toml       # Cloudflare Workers Configuration
└── vitest.config.ts    # Test Environment Configuration
```


# Execution Schedule (Cron Triggers)
 This bot utilizes Cloudflare Workers Scheduled Events to optimize resource usage. Instead of running 24/7, it activates precisely at the 1st and 31st minute of every hour to match the game's data refresh cycle.
  - Schedule: 1,31 * * * * (Cron Expression)
  - Workflow:
    1. The Worker wakes up automatically at the scheduled time.
    2. Fetches the latest TZ/DC data from the APIs.
    3. Analyzes the data and triggers a Discord notification only if there are relevant changes.
    4. Immediately


# Configuration (Environment Variables)
- Configure the following secrets in your Cloudflare Workers dashboard or .dev.vars file:

|Variable|Description|
|---|---|
|TERROR_ZONE_API_URL|API endpoint for Terror Zone data|
|DIABLO_CLONE_API_URL|API endpoint for Diablo Clone progress|
|D2TZ_TOKEN|[Authentication token for the APIs](<https://www.d2tz.info/api>)|
|DISCORD_WEBHOOKS|Discord Webhook URLs (Comma-separated if multiple)|

# Data courtesy
Data courtesy of [d2tz.info](<https://www.d2tz.info/>)

# Running Tests
The business logic is fully verified using Vitest.
```
npm test
```

# Deployment
```
# Start local development environment
npx wrangler dev
```