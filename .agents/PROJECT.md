# Project: NuKropAI Android App Audit & Fixes

## Architecture
- **Framework**: Android Jetpack Compose + Kotlin Coroutines & StateFlow
- **UI Architecture**: Single-Activity (`MainActivity.kt`) with Navigation Bar + Compose Navigation / Screen Switching
- **Backend Integrations**:
  - **Groq AI Vision & Chat**: `GeminiVisionService.kt` for agricultural diagnostic vision and conversational assistance
  - **Supabase DB & Auth**: `SupabaseClient.kt` for cloud persistence across mandi rates, user profiles, peer chat, equipment rental, and khata ledger
  - **Agmarknet Mandi API**: `MandiApiService.kt` for government mandi commodity market rates
  - **Open-Meteo Weather API**: `WeatherService.kt` for local agricultural weather forecast
- **State Management**: Android ViewModels (`AuthViewModel`, `ChatViewModel`, `MarketViewModel`, `ScannerViewModel`, `WeatherViewModel`, `KhataViewModel`, etc.)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Root Scaffold & Window Insets | Fix double status bar padding by configuring root Scaffold contentWindowInsets | M1 | UI Survey |
| 2 | IME Keyboard Insets | Add imePadding to text inputs on Chat, PeerChat, and Login screens | M1 | UI Survey |
| 3 | Row Child Weights & Overflow | Add weight(1f) and text ellipsis to horizontal cards (Mandi, PeerChat, Profile, Khata, Equipment, Reports) | M1 | UI Survey |
| 4 | Responsive Scrolling on Fixed Screens | Add verticalScroll to ScanHub, TractorAutopilot, Splash, DevicePairing | M1 | UI Survey |
| 5 | Bounded Height in Nested Lists | Add weight(1f) to nested LazyColumns (KnowledgeScreen) | M1 | UI Survey |
| 6 | Scrollable List Bottom Clearance | Ensure bottom padding/Spacer (80.dp) across all LazyColumns and scrollable lists to clear bottom navigation bar | M1 | ORIGINAL_REQUEST §Acceptance Criteria & UI Survey |
| 7 | Groq AI Active Model IDs | Update obsolete 404 model IDs to verified active models (groq/compound-mini, qwen/qwen3.6-27b, openai/gpt-oss-20b) | M2 | API Survey |
| 8 | Groq Error Recovery & Reasoning Parsing | Relax loop break on non-429 errors; strip <think> tags before JSON parsing | M2 | API Survey |
| 9 | Agmarknet Key Rotation Lockup Fix | Repair key rotation logic in MandiApiService to prevent 403 Forbidden lockups from unauthorized secondary keys | M2 | API Survey |
| 10 | ViewModel State Safety & Infinite Loading | Ensure all ViewModels handle errors and reset isLoading in finally blocks | M2 | ORIGINAL_REQUEST §R2 |
| 11 | Environment & Secrets Documentation | Populate .env.example with reference template keys | M2 | API Survey |
| 12 | Compilation & Build Verification | Verify ./gradlew assembleDebug passes cleanly with 0 errors | M3 | ORIGINAL_REQUEST §Acceptance Criteria |
| 13 | Independent Spacing & Network Review | Independent reviewer verification of scroll padding and network syntax | M3 | ORIGINAL_REQUEST §Acceptance Criteria |
| 14 | Forensic Integrity Audit | Systematic integrity audit confirming authentic implementations | M3 | Audit Protocol |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: UI Alignment & Polish | Fix Scaffold insets, IME padding, Row child weights, vertical scrolling, and bottom list clearance (80.dp) across all screens | none | IN_PROGRESS |
| 2 | M2: Bug Squashing & API Stability | Fix Groq model IDs, loop recovery, <think> parsing, Agmarknet key rotation, and ViewModel state safety | none | PLANNED |
| 3 | M3: Build Verification & Multi-Agent Gate | Run ./gradlew assembleDebug, independent reviewer evaluations, challenger stress checks, and forensic audit | M1, M2 | PLANNED |

## Interface Contracts
### UI ↔ Navigation & Inset Boundaries
- Root `Scaffold` must not consume status bar insets (`contentWindowInsets = WindowInsets(0.dp)`), allowing individual screen top bars to use `.statusBarsPadding()`.
- Bottom navigation bar height is ~64–80dp. All scrollable lists (`LazyColumn`, `LazyVerticalGrid`, scrollable `Column`) must provide `80.dp` bottom clearance (`contentPadding = PaddingValues(bottom = 80.dp)` or trailing `Spacer(Modifier.height(80.dp))`).

### Groq AI ↔ Diagnostic & Chat Services
- `GeminiVisionService` must send requests to active Groq models (`groq/compound-mini`, `qwen/qwen3.6-27b`, `openai/gpt-oss-20b`).
- `parseText()` must strip `<think>.*?</think>` before JSON extraction.
- HTTP error handling must attempt next available keys/models rather than aborting prematurely on non-429 codes.

### MandiApiService ↔ Agmarknet API
- Key 1 (`579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b`) is authorized; unauthorized keys must not lock the service into permanent 403 errors.

## Code Layout
- `app/src/main/java/com/example/`
  - `MainActivity.kt`: Root scaffold and navigation bar
  - `HomeScreen.kt`, `MarketScreen.kt`, `DiseaseScannerScreen.kt`, `LoanScreen.kt`, `ProfileScreen.kt`, `ChatScreen.kt`, `PeerChatScreen.kt`, `FarmKhataScreen.kt`, `EquipmentRentalScreen.kt`, `SavedReportsScreen.kt`, `KnowledgeScreen.kt`, `DroneOpsScreen.kt`, `AgentsScreen.kt`, `FoodSecurityScreen.kt`, `RegionalIntelligenceScreen.kt`, `ScientificValidationScreen.kt`, `TractorAutopilotScreen.kt`, `SplashScreen.kt`, `DevicePairingScreen.kt`, `LoginScreen.kt`: Jetpack Compose Screens
  - `GeminiVisionService.kt`: Groq AI service
  - `MandiApiService.kt`: Agmarknet service
  - `SupabaseClient.kt`: Supabase database & auth
  - `WeatherService.kt`: Open-Meteo weather service
  - ViewModels: `AuthViewModel.kt`, `MarketViewModel.kt`, etc.
