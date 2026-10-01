# Project: NuKropAI Agrarian OS Production-Ready Upgrade

## Architecture
- **Platforms**:
  - **Android Native**: Kotlin, Jetpack Compose, CameraX, Supabase-kt, ExoPlayer/WebView, Retrofit/OkHttp, TFLite ML inference (`DiseaseDetector.kt`).
  - **Web Emulator & WebView Runtime**: `app/src/main/assets/index.html` (Android embedded asset) and `nukrop_emulator.html` (Web preview).
  - **Backend Cloud**: Supabase Cloud (`https://yxjqseiegwjdfnccdchk.supabase.co`) with GoTrue v2.196.0, PostgREST tables (`user_profiles`, `community_posts`, `mandi_live_rates`, `disease_scans`), and Cloud Storage bucket (`community-media`).
  - **Multimodal AI**: Google Generative Language API (`gemini-1.5-flash:generateContent`) with `inlineData` image payload, JSON grammar enforcement, and on-device TFLite fallback.
  - **Agricultural Market Engine**: Live Agmarknet APMC rates via Government of India portal (`api.data.gov.in`) + Supabase persistent live cache + GPS location reverse-geocoding.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Supabase Live Authentication | Real GoTrue auth for Sign Up (with user metadata name), Email/Password Login, and Google OAuth | M1 | Survey (R1) |
| 2 | Persistent Session & Identity Rehydration | Resilient session recovery preventing cold start preference wipes; local rehydration across Android prefs and Web localStorage | M1 | Survey (R1) |
| 3 | Dynamic User Name & Greeting Display | Display user name and personalized greeting in App Header and Profile Screen across Compose and Web | M1 | Survey (R1) |
| 4 | Gemini Vision API Integration | Connect Crop & Soil Scanner to Google Generative Language API (`gemini-1.5-flash:generateContent`) with `inlineData` image payload | M2 | Survey (R2) |
| 5 | Dynamic Environment Key Resolution | Sourcing `GEMINI_API_KEY` via `BuildConfig.GEMINI_API_KEY`, `System.getenv`, and `window.GEMINI_API_KEY` with zero hardcoded secret leakage | M2 | Survey (R2) |
| 6 | Resilient Diagnostic Parsing & On-Device TFLite Fallback | Structured JSON diagnostic parsing (`CropScanData`, `SoilScanData`) with automatic fallback to on-device `DiseaseDetector` | M2 | Survey (R2) |
| 7 | Community Post Media Capture & File Chooser | Native Android & Web file chooser supporting real photo and video capture / selection (no mock string literals) | M3 | Survey (R3) |
| 8 | Community Media Cloud Storage & Database Schema | Add `media_url` and `media_type` to `public.community_posts`; set up `community-media` storage bucket | M3 | Survey (R3) |
| 9 | Community Feed Video Player & Photo Gallery | Real `<video>` tag playback with controls and responsive `<img src>` rendering in Web feed & Compose card | M3 | Survey (R3) |
| 10 | Real Agmarknet Market Data API | Fetch real live daily mandi prices from `api.data.gov.in` + Supabase `mandi_live_rates` catalog with error backoff | M4 | Survey (R4) |
| 11 | Location-Driven Mandi Integration | Reverse-geocode user GPS coordinates to state/district and query real local APMC mandi market rates | M4 | Survey (R4) |
| 12 | Synthetic / Mock Price Generator Eradication | Completely eliminate `Math.random() * 50` and synthetic `dyn-` prices from the codebase | M4 | Survey (R4) |
| 13 | Comprehensive E2E Opaque-Box Acceptance Test Suite | Systematic 4-tier test suite covering Auth, Scanner, Community, and Mandi workflows with zero mock bypass | M5 | Survey (Acceptance) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Live Supabase Authentication & Persistent Identity | Real Supabase auth (Sign Up, Email, Google), cold start session rehydration, header & profile user name display | none | IN_PROGRESS |
| M2 | Gemini Vision AI Integration & Resilient Scanner | Google Generative Language API migration, dynamic API key resolution, inlineData payload, on-device TFLite fallback | none | PLANNED |
| M3 | Kisan Community Media Feed & Video Engine | Real image/video upload chooser, Supabase DB & Storage media columns, video player and photo rendering | none | PLANNED |
| M4 | Real Agmarknet Market Data & Mandi Arbitrage | Real Gov API + Supabase APMC rates, GPS location integration, eradication of synthetic mock price generators | none | PLANNED |
| M5 | Final E2E Test Suite & Adversarial Hardening | Tier 1-4 opaque-box acceptance test suite, test runner, adversarial verification, integrity audit | M1, M2, M3, M4 | PLANNED |

## Interface Contracts
### AuthViewModel ↔ ProfileScreen / HomeScreen
- Data Model: `data class NuKropUser(val id: String, val email: String, val name: String, val avatarUrl: String? = null)`
- StateFlow: `val currentUser: StateFlow<NuKropUser?>`
- Invariant: App start must NOT clear SharedPreferences when `sessionStatus` is Initializing/NotAuthenticated. Rehydrate from local cache immediately.

### GeminiVisionService ↔ DiseaseScannerScreen
- Endpoint: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}`
- API Key Resolution: Parameter `apiKey` -> `BuildConfig.GEMINI_API_KEY` -> `System.getenv("GEMINI_API_KEY")`.
- Resilient Fallback: If network/key fails, decode bitmap and execute `DiseaseDetector(context).classifyToScanData(bitmap)`.

### Community Engine ↔ Feed UI
- Supabase Table `public.community_posts`: Columns `media_url TEXT`, `media_type TEXT` ('image' | 'video').
- Web File Input: `<input type="file" accept="image/*,video/*">` uploads binary to Supabase Storage `community-media` or Base64 preview.
- Feed Rendering: Render `<video controls playsinline>` if `media_type === 'video'` or URL ends in `.mp4`; else `<img src>`.

### Mandi Market Engine ↔ Agmarknet & Location
- GPS Integration: `window.onNativeLocationReceived(lat, lon)` sets `mandiSearchState` and `mandiSearchMandi` and triggers `fetchLiveMandiData(crop, state, district)`.
- Resilient Pipeline: Query Supabase `mandi_live_rates` -> `api.data.gov.in` (Key 1 with 429 backoff) -> regional benchmark averages. Zero `Math.random()`.

## Code Layout
- Android Native Kotlin (`app/src/main/java/com/example/`):
  - `AuthViewModel.kt`, `ProfileScreen.kt`, `HomeScreen.kt`, `SupabaseClient.kt` (M1)
  - `GeminiVisionService.kt`, `DiseaseScannerScreen.kt`, `GeminiApi.kt`, `ml/DiseaseDetector.kt` (M2)
  - `CommunityScreen.kt`, `MainActivity.kt` (M3)
  - `MandiApiService.kt`, `MarketScreen.kt`, `mandipilot/MandiPilotEngine.kt`, `mandipilot/MandiPilotScreen.kt` (M4)
  - `app/build.gradle.kts` (M2 `buildConfigField`)
- Web Assets & Emulator:
  - `app/src/main/assets/index.html` (M1, M2, M3, M4)
  - `nukrop_emulator.html` (M1, M2, M3, M4)
- Verification & Test Suites:
  - `test_full_flow.js`, `test_home.js`
  - `app/src/test/java/com/example/`
