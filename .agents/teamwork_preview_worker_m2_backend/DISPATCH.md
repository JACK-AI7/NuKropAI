## 2026-08-24T16:33:27Z
You are the Bug Squashing & API Stability Worker (teamwork_preview_worker) for NuKropAI Android App.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2_backend
Workspace root: c:\Users\bjasw\Downloads\agriculture-ai-os

Mandatory input files to read first:
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\PROJECT.md
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_api\survey_api_report.md
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_bugs_3\survey_bugs_report.md

Your Assigned Scope (Milestone M2: Bug Squashing & API Stability):
You have exclusive write ownership of Backend, Network, ViewModel, and Service files:
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

Tasks to execute:
1. Groq AI Service Updates (GeminiVisionService.kt):
   - Update model IDs to currently active Groq models: `groq/compound-mini`, `qwen/qwen3.6-27b`, `openai/gpt-oss-20b`.
   - Strip `<think>.*?</think>` reasoning tags in `parseText()` before JSON parsing.
   - Fix error loop control flow: do not break prematurely on non-429 HTTP status codes; allow rotation across fallback keys and models.
2. Agmarknet Mandi API Service (MandiApiService.kt):
   - Repair key rotation logic: Key 1 (`579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b`) is the primary active key. Ensure that 403 or 429 errors gracefully fall back to cached Supabase data (`mandi_live_rates`) and memory cache (`lastGoodData`) without locking the app into permanent 403 failure loops on unauthorized keys.
3. SupabaseClient URL Encoding & Safety:
   - In SupabaseClient.kt, use `URLEncoder.encode(..., "UTF-8")` for all dynamic query parameters (state, commodity) to avoid IllegalArgumentException crashes on strings with spaces or special characters.
4. UpdateManager Threading Fix (UpdateManager.kt):
   - In `checkAndUpdate()`, wrap the `Toast.makeText(...).show()` call in `withContext(Dispatchers.Main)` so it does not throw `Can't toast on a thread that has not called Looper.prepare()`.
5. ChatViewModel Infinite Loading & State Safety (ChatViewModel.kt):
   - In `sendMessage()`, wrap the coroutine launch body in `try ... finally { _generatingStatus.value = "" }` and handle any uncaught exception so that `_generatingStatus` is always cleared, preventing permanent UI lockout.
6. PriceTickerService Shimmer & Lifecycle Fix (PriceTickerService.kt):
   - Ensure `_isLoading` is set to `false` even if the initial network fetch is empty/fails.
   - In `start()` and `stop()`, manage a nullable `tickerJob: Job?` instead of cancelling the entire `CoroutineScope`, allowing the service to restart cleanly.
7. OkHttp ResponseBody Resource Leak Prevention:
   - Enclose `client.newCall(...).execute()` in `.use { response -> ... }` across GeminiVisionService.kt, SupabaseClient.kt, WeatherService.kt, UpdateManager.kt, etc., to avoid socket and connection leaks.
8. NuKropIotManager Concurrency:
   - Protect `offlineCommandQueue` against concurrent modification (e.g. `ConcurrentLinkedQueue`) and replace unmanaged OS threads with managed coroutine delay jobs.
9. AuthViewModel State Sync & User Model:
   - Ensure `_authState` resets to `AuthState.Idle` on session expiration/logout.
   - Cleanly type user representation to support ProfileScreen display.
10. Secrets Documentation (.env.example):
    - Populate `.env.example` with template keys for `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `AGMARKNET_API_KEY`.
11. Verify compilation by running `./gradlew compileDebugKotlin` or `./gradlew assembleDebug` via run_command. Ensure 0 build errors.
12. Write `handoff.md` and `progress.md` in your working directory and notify the parent orchestrator with send_message.
