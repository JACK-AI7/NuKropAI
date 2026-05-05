# NuKropAI — Mobile-First Architecture (No Backend AI)

## New Design
- **All AI runs on-device or via direct cloud API from mobile** — no backend AI processing
- Backend is optional: only for user accounts & scan history sync
- Real-time weather fetched directly from Open-Meteo on mobile
- On-device LLM via Gemini API (cloud) or future GGUF integration

## Changes Ahead
1. Remove YOLO Python service & Node wrapper
2. Simplify ScanController to accept pre-analyzed results from mobile
3. Mobile does all analysis locally/cloud directly
4. Weather fetched directly on mobile
5. Polish UI across scanner & results screens
