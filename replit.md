# NuKropAI

An AI-powered farming platform for Indian farmers — crop disease detection via camera/gallery, multilingual AI chat assistant (EN/HI/TE), weather intelligence, analytics, and farmer profile management.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 8080)
- `pnpm --filter @workspace/mobile run dev` — run the Expo mobile app
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL`, `AI_INTEGRATIONS_OPENAI_BASE_URL`, `AI_INTEGRATIONS_OPENAI_API_KEY`

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Mobile: Expo SDK 54, React Native, expo-router, react-native-reanimated
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- AI: OpenAI via Replit AI Integrations (`gpt-5-mini` for chat)
- Validation: Zod (`zod/v4`), `drizzle-zod`
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/mobile/` — Expo app
  - `app/(tabs)/` — 5 tab screens: index (home), scanner, chat, analytics, profile
  - `components/` — GlassCard, WeatherCard, AIInsightCard, PulseIndicator, ScanResultCard, MessageBubble, StatCard
  - `contexts/AppContext.tsx` — global state (farmer profile, language, scan history, chat history)
  - `constants/colors.ts` — dark green premium theme
- `artifacts/api-server/src/routes/chat.ts` — `POST /api/chat` AI farming assistant endpoint
- `lib/integrations-openai-ai-server/` — Replit AI OpenAI client

## Architecture decisions

- Dark-mode-only app forced via `Appearance.setColorScheme("dark")` (guarded for web compatibility)
- AI chat is stateless on the server — message history sent from the client for context, no DB storage needed
- Scanner uses expo-image-picker for both camera and gallery; disease detection is AI-simulated on device (mock results with realistic disease data)
- AsyncStorage persists farmer name, language preference, scan history, and chat history across app restarts
- Web platform renders correctly with explicit top/bottom padding overrides (67px top, 84px tab bar)

## Product

NuKropAI gives farmers:
1. **AI Scanner** — photograph a crop leaf to get instant disease diagnosis with confidence score, severity, affected area %, and treatment recommendations
2. **AI Chat** — ask farming questions in English, Hindi, or Telugu and receive expert AI advice powered by GPT-5-mini
3. **Weather Intelligence** — weather card with temperature, humidity, wind speed, UV index, and AI crop recommendation
4. **Analytics** — disease breakdown charts, weekly scan trends, and AI-generated weekly recommendations
5. **Profile** — editable farmer name, farm location, language selection, and chat history management

## User preferences

- Dark forest green premium aesthetic (`#060C09` background, `#22C55E` primary)
- Futuristic, cinematic, production-grade quality
- Multilingual: English, Hindi, Telugu

## Gotchas

- `Appearance.setColorScheme` is not available on web — must guard with `typeof === "function"` check
- API server runs on port 8080; mobile accesses it via `EXPO_PUBLIC_DOMAIN` env var
- Do not use `AnimatedStyle` hooks inside `.map()` — extract into separate components (e.g. `AnimBar`, `ColBar`, `ScanRing`)

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
- See the `ai-integrations-openai` skill for adding more AI features
