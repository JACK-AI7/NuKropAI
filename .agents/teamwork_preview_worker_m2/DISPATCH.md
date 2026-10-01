# Dispatch: Worker M2 (Milestone 2 - Dynamic Pest and Disease Alerts)
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2
Original Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Survey Report: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_2_gen2\handoff.md
Project Index: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective: Implement Milestone 2 (R2 - Dynamic Pest and Disease Alerts)
1. **Purge All Hardcoded "Warangal" Fallbacks**:
   - In `nukrop_emulator.html` and `app/src/main/assets/index.html`, purge every hardcoded fallback to "Warangal", "Telangana", or static districts across:
     - `PEST_SURVEILLANCE_ALERTS` (lines ~2296–2339): replace hardcoded Warangal trap strings with dynamic state/district placeholders.
     - `REAL_MARKET_TICKER_ITEMS` (line ~4041): change `mandi: 'Warangal Cluster'` to dynamically bind to the user's active/detected cluster.
     - `fetchRealLocationAndWeather()` (line ~6634): remove `|| 'Warangal'` and `|| 'Telangana'`.
     - `onNativeLocationReceived()`: remove `|| 'Telangana'`.
     - Onboarding Step 4 and Notification Center: remove static Warangal strings.
2. **Implement Resilient Location Resolution Hierarchy**:
   - Implement `getEffectiveUserState()` with 4-tier resolution:
     1. Live geocoded state from GPS / OpenStreetMap Nominatim (`liveWeather.detectedState`).
     2. Saved farm profile state from `farmerProfile.state` or `localStorage.getItem('nukrop_user_state')`.
     3. Active search state from Mandi selector.
     4. Neutral prompt / National overview (e.g. `'National'` or prompt user). NEVER inject "Warangal" unprompted.
3. **Dynamic Pest Alert Engine**:
   - Implement `fetchDynamicPestAlerts(targetState, targetDistrict)`:
     - Attempts PostgREST query to `${SUPABASE_CONFIG.url}/rest/v1/outbreak_alerts?target_state=eq.${encodeURIComponent(state)}&is_active=eq.true&order=scan_count.desc`.
     - Fallback: Evaluates in-memory regional pest matrix (`getRegionalPestMatrix(state, district)`) tailored for that state's primary crops (e.g. Maharashtra -> Cotton Pink Bollworm & Soybean Stem Fly; Punjab -> Wheat Yellow Rust & Paddy Stem Borer; Gujarat -> Cotton Whitefly & Groundnut Tikka; Telangana -> Chilli Thrips & Cotton Bollworm).
     - Dynamically updates `PEST_SURVEILLANCE_ALERTS`.
     - Updates the news ticker item (`type: 'alert'`) to display the real state/district sector.
     - Updates Home view alert badge and BioShield view in real-time.
4. **Maintain Exact Parity**:
   - Apply every change symmetrically to both `nukrop_emulator.html` and `app/src/main/assets/index.html`.
5. **Automated Verification**:
   - Create and run `tests/verify_milestone2_pest_alerts.js` testing:
     - 0 hardcoded "Warangal" in alert data, ticker, or geocoding fallbacks.
     - Dynamic state switching (e.g. simulating Maharashtra, Punjab, Telangana) updates alert cards and ticker.
     - `node test_production_readiness.js` passes with zero regressions.
6. **Handoff Report**:
   - Write report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2\handoff.md`.
   - Send message to parent with path and test outputs.

## 2026-09-09T08:57:30Z
User Request:
Implement Milestone 2: Dynamic Pest and Disease Alerts without Hardcoded Fallbacks.
1. Purge all hardcoded "Warangal" fallbacks and static district strings from `nukrop_emulator.html` and `app/src/main/assets/index.html`.
2. Implement `getEffectiveUserState()` hierarchy (GPS -> Profile -> Mandi Search -> National neutral; never static Warangal).
3. Implement `fetchDynamicPestAlerts(state, district)` dynamically querying Supabase and regional matrix, updating `PEST_SURVEILLANCE_ALERTS`, BioShield view, and ticker item.
4. Wire location updates (`fetchRealLocationAndWeather` and `onNativeLocationReceived`) to trigger dynamic pest alert refresh.
5. Maintain 100% parity across `nukrop_emulator.html` and `app/src/main/assets/index.html`.
6. Write and run `tests/verify_milestone2_pest_alerts.js` and verify `node test_production_readiness.js` passes with 0 regressions.
7. Write your handoff report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2\handoff.md` and notify parent.

## 2026-09-09T09:10:14Z
Parent Agent Message:
Heartbeat check on Milestone 2 progress. Please report your current step: have you finished implementing `getEffectiveUserState()`, `fetchDynamicPestAlerts()`, purging Warangal references across nukrop_emulator.html and app/src/main/assets/index.html, and running the verification tests?
Action: Please update progress.md and advise on estimated time to handoff.

