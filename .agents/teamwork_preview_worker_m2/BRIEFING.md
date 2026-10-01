# BRIEFING — 2026-09-09T08:58:00Z

## Mission
Implement Milestone 2: Dynamic Pest and Disease Alerts without Hardcoded Fallbacks. Purge hardcoded "Warangal" strings, implement getEffectiveUserState() hierarchy, implement fetchDynamicPestAlerts(state, district), wire location updates, maintain parity with app/src/main/assets/index.html, and verify with tests.

## 🔒 My Identity
- Archetype: implementer
- Roles: implementer, qa, specialist
- Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2
- Original parent: 5a562a6e-e085-45d6-b37c-583c7f1f5733
- Milestone: M2 (Market Impact Calculator & Domain Models)
- Appended Identity (2026-09-09): Worker M2 (teamwork_preview_worker), Parent: 9fe7eb84-632a-4cec-a18b-59310aa6bae6, Milestone: M2 (Dynamic Pest and Disease Alerts)

## 🔒 Key Constraints
- Exclusively Owned Files:
  - `app/src/main/java/com/example/market/MarketImpactModels.kt`
  - `app/src/main/java/com/example/market/MarketImpactCalculator.kt`
  - `app/src/main/java/com/example/market/MarketImpactRepository.kt`
- Deterministic econometric engine with crop perishability map, severity shocks, density saturation, and geographic multipliers.
- Compatible with `com.example.model.OutbreakAlert` and `com.example.MandiRecord`.
- Must verify with `./gradlew assembleDebug`.
- Appended Constraints (2026-09-09):
  - Purge all hardcoded "Warangal" fallbacks and static district strings from `nukrop_emulator.html` and `app/src/main/assets/index.html`.
  - Implement `getEffectiveUserState()` hierarchy (GPS -> Profile -> Mandi Search -> National neutral; never static Warangal).
  - Implement `fetchDynamicPestAlerts(state, district)` dynamically querying Supabase and regional matrix, updating `PEST_SURVEILLANCE_ALERTS`, BioShield view, and ticker item.
  - Wire location updates (`fetchRealLocationAndWeather` and `onNativeLocationReceived`) to trigger dynamic pest alert refresh.
  - Maintain 100% parity across `nukrop_emulator.html` and `app/src/main/assets/index.html`.
  - Write and run `tests/verify_milestone2_pest_alerts.js` and verify `node test_production_readiness.js` passes with 0 regressions.
  - Mandatory Integrity Mandate: Genuine implementation, no cheating, no hardcoding test results.

## Current Parent
- Conversation ID: 9fe7eb84-632a-4cec-a18b-59310aa6bae6
- Updated: 2026-09-09T08:58:00Z

## Task Summary
- **What to build**: Dynamic pest and disease alerts engine, resilient 4-tier location hierarchy, purging Warangal fallbacks across HTML emulator and Android assets.
- **Success criteria**: 0 hardcoded Warangal fallbacks in alerts/ticker/location, dynamic updates on GPS/profile change, tests pass, zero regressions on `node test_production_readiness.js`.
- **Interface contracts**: PROJECT.md § LocationEngine ↔ Dynamic Pest Alerts
- **Code layout**: `nukrop_emulator.html`, `app/src/main/assets/index.html`, `tests/verify_milestone2_pest_alerts.js`

## Key Decisions Made
- [In progress] Reviewing all occurrences of "Warangal" and alert logic in `nukrop_emulator.html` and `app/src/main/assets/index.html`.

## Change Tracker
- **Files modified**: None yet
- **Build status**: Pending
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pending
- **Lint status**: Pending
- **Tests added/modified**: `tests/verify_milestone2_pest_alerts.js` (planned)

## Artifact Index
- `.agents/teamwork_preview_worker_m2/DISPATCH.md`
- `.agents/teamwork_preview_worker_m2/BRIEFING.md`
- `.agents/teamwork_preview_worker_m2/progress.md`
- `.agents/teamwork_preview_worker_m2/handoff.md`
