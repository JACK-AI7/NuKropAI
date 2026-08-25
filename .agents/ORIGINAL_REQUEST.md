# Original User Request

## 2026-08-24T16:30:23Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Use a very large team of agents (App senior maker, alignment checker, bug fixer, and API token checker)

Thoroughly audit and fix the NuKropAI Android app. The team must fix any remaining UI alignment issues, resolve any lingering bugs, and verify that all API tokens and connections (Groq AI, Supabase, Agmarknet) are functioning correctly. Use a very large team of agents.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: development

## Requirements

### R1. UI Alignment & Polish
Audit all Jetpack Compose screens (Home, Market, Profile, Scanner, Loan, etc.) for text overflow, missing padding, or overlapping elements (especially with the bottom navigation bar) and fix them.

### R2. Bug Squashing
Review the Kotlin codebase for any crashes, infinite loading states, or logical errors and apply fixes.

### R3. API Token & Connection Verification
Test and verify that the Groq AI keys, Supabase DB credentials, and Agmarknet API endpoints are correctly formatted, not rate-limited, and successfully fetching data.

## Acceptance Criteria

### Verification (Agent-as-Judge & Compilation)
- [ ] An independent reviewer agent must read the modified UI code and confirm that proper spacing (e.g., `Spacer` or `padding`) is applied at the bottom of all scrollable lists.
- [ ] An independent reviewer agent must verify that API keys are correctly formatted strings and the network request logic does not contain obvious syntax errors.
- [ ] A test compilation (`./gradlew assembleDebug` or similar script) must pass without syntax errors to prove the codebase remains structurally sound after the fixes.

## 2026-08-25T13:41:52Z

This is a single self-contained fix; keep it small and focused.

Fix UI alignment issues in the NuKropAI Android app (Jetpack Compose). The app is at: c:\Users\bjasw\Downloads\agriculture-ai-os

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: development

## Requirements

### R1. Bottom Padding on All Scrollable Screens
The following Kotlin screens are missing bottom padding and their content gets hidden behind the bottom navigation bar. Add `padding(bottom = 120.dp)` (or equivalent `contentPadding` for LazyColumn) to every scrollable container (Column with verticalScroll, or LazyColumn) in each file:

- app/src/main/java/com/example/AgentsScreen.kt
- app/src/main/java/com/example/DevicePairingScreen.kt
- app/src/main/java/com/example/FarmDigitalTwinScreen.kt
- app/src/main/java/com/example/FoodSecurityScreen.kt
- app/src/main/java/com/example/KnowledgeScreen.kt
- app/src/main/java/com/example/PeerChatScreen.kt
- app/src/main/java/com/example/RegionalIntelligenceScreen.kt
- app/src/main/java/com/example/ScientificValidationScreen.kt
- app/src/main/java/com/example/SoilScreen.kt

Do NOT modify LoginScreen.kt or SplashScreen.kt (they are full-screen auth flows with no nav bar).

### R2. Build Verification
After making all edits, run `./gradlew assembleDebug` from the working directory. The build must succeed (exit code 0). If it fails, fix the compile errors and rebuild until it passes.

### R3. Deploy
Once the build passes:
1. Copy `app/build/outputs/apk/debug/app-debug.apk` to `web/public/NuKropAI_v2.0.apk`
2. Run: `git add . && git commit -m "fix: Add bottom padding to remaining 9 screens for nav bar alignment" && git push origin main`

## Acceptance Criteria

### Build
- [ ] `./gradlew assembleDebug` exits with code 0
- [ ] No new compile errors introduced

### Padding
- [ ] Every file listed in R1 has at least one `bottom = 120.dp` or `bottom = 100.dp` padding applied to its main scrollable container
- [ ] LoginScreen.kt and SplashScreen.kt are NOT modified

