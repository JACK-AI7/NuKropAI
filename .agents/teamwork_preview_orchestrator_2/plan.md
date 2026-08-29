# NuKropAI National Crop Disease Aggregation & Early Warning System — Orchestration Plan

## 1. Survey & Scope Mapping (Phase 0)
- Dispatch 3 parallel Explorers:
  1. `explorer_backend`: Investigate database schema, backend architecture (Supabase / PostgreSQL migrations / Edge functions / Kotlin repos / network layer), scan storage & aggregation mechanisms.
  2. `explorer_market`: Investigate market/mandi pricing models, crop price calculators, outbreak impact prediction logic.
  3. `explorer_android_ui`: Investigate Android app structure, on-device scan result flow, Home screen, Market screen Compose UI, viewmodels, and DI/repositories.

## 2. Project Decomposition (Phase 1)
- Formulate comprehensive `PROJECT.md` with:
  - Architecture and feature inventory
  - Milestone decomposition (M1: Database & Backend Aggregation / Alerts; M2: Market Impact Calculator; M3: Android App Scan Push & UI Integration; M4: E2E Test Suite & Full Verification)
  - Code layout & interface contracts

## 3. Dual Track Execution (Phase 2)
- E2E Testing Track: Build test infrastructure and verify 100 scan threshold logic, market impact predictions, UI data flow.
- Implementation Track: Execute milestones via Explorer -> Worker -> Reviewer -> Challenger -> Auditor cycle.

## 4. Verification & Audit (Phase 3)
- Validate `./gradlew assembleDebug` clean build.
- Validate 100-scan density threshold triggers early warning alert for neighboring areas.
- Forensic Auditor integrity verification.

## 5. Synthesis & Handover (Phase 4)
- Report final findings and verification results to Sentinel.
