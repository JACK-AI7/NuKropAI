# BRIEFING — 2026-08-24T16:34:00Z

## Mission
Execute Milestone M2 (Bug Squashing & API Stability) for NuKropAI Android App across Backend, Network, ViewModel, and Service layers.

## 🔒 My Identity
- Archetype: teamwork_preview_worker
- Roles: implementer, qa, specialist
- Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2_backend
- Original parent: 033ac0ee-855c-4da0-b225-ede6c53629b8
- Milestone: M2 - Bug Squashing & API Stability

## 🔒 Key Constraints
- Exclusive write ownership:
  - app/src/main/java/com/example/GeminiVisionService.kt
  - app/src/main/java/com/example/MandiApiService.kt
  - app/src/main/java/com/example/SupabaseClient.kt
  - app/src/main/java/com/example/WeatherService.kt
  - app/src/main/java/com/example/UpdateManager.kt
  - app/src/main/java/com/example/PriceTickerService.kt
  - app/src/main/java/com/example/ChatViewModel.kt
  - app/src/main/java/com/example/AuthViewModel.kt
  - app/src/main/java/com/example/telemetry/NuKropIotManager.kt
  - .env.example
- DO NOT CHEAT. Real genuine fixes only. No fake mocks or hardcoded tests.
- Verify compilation with Gradle.

## Current Parent
- Conversation ID: 033ac0ee-855c-4da0-b225-ede6c53629b8
- Updated: 2026-08-24T16:34:00Z

## Task Summary
- **What to build**: Fix Groq model IDs, strip `<think>` tags, fix AI key/model fallback rotation, fix Mandi API key rotation & cache fallback, URL-encode Supabase query params, fix UpdateManager toast threading, fix ChatViewModel infinite loading state safety, fix PriceTickerService shimmer/lifecycle, fix OkHttp ResponseBody resource leaks, fix NuKropIotManager concurrency/threads, fix AuthViewModel state sync and user model, document secrets in .env.example.
- **Success criteria**: All 10 tasks cleanly implemented, project compiles cleanly with 0 build errors (`./gradlew compileDebugKotlin` / `./gradlew assembleDebug`), handoff and progress reports written, parent notified.
- **Interface contracts**: PROJECT.md, survey reports.
- **Code layout**: Android app module under `app/src/main/java/com/example/`

## Key Decisions Made
- [TBD - will populate as tasks proceed]

## Artifact Index
- DISPATCH.md — Assignment instructions
- BRIEFING.md — Situational awareness
- progress.md — Liveness & task progress
- handoff.md — Final 5-component handoff report

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: Initializing fixes

## Quality Status
- **Build/test result**: Pending verification
- **Lint status**: Clean
- **Tests added/modified**: TBD

## Loaded Skills
- None required to be loaded externally
