# Plan: NuKropAI Fullstack Audit & Hardening Sweep

## Objectives
1. Perform exhaustive code and spec survey to inventory all features across emulator, Kotlin core, and Supabase backend.
2. Establish Dual-Track execution:
   - Implementation Track: R1 (Live Data Pipeline), R2 (16 OS Views & Features), R3 (i18n & Single-Language Dropdowns).
   - E2E Testing Track: Automated testing covering all 176 views (16 screens x 11 languages), spray 3h window calculation, single-language dropdowns, Android build check.
3. Rigorous gating: Explorer -> Worker -> Reviewer -> Challenger -> Forensic Auditor cycle for each milestone.
4. Pass 100% automated E2E tests, complete DPDP Act 2023 audit, and report back to Sentinel.

## Phases
1. **Phase 0: Survey (3 parallel explorers/spec miners)**
   - Explorer 1 (Spec Miner): Extract requirements from ORIGINAL_REQUEST.md, identify all 16 views, 11 languages, and specific calculation rules (spray 3h window, crop selector, DPDP compliance).
   - Explorer 2 (Architecture & Data Pipelines): Map codebase layout, ukrop_emulator.html, Kotlin files, Supabase integration, Agmarknet, weather sensors, OpenFarm, AgriStack, and identify dummy mocks or placeholders.
   - Explorer 3 (i18n & Test Harness): Map language dropdowns, i18n keys across all 11 Indian languages, test runners, and build systems.
2. **Phase 1: Project Decomposition & Test Infra Setup**
   - Synthesize findings into `PROJECT.md` and `TEST_INFRA.md`.
3. **Phase 2: Milestone Iteration Loops (Worker -> Reviewers -> Challengers -> Auditor)**
4. **Phase 3: Final E2E Test Suite Pass & Adversarial Coverage Hardening**
5. **Phase 4: Final Victory Audit & Sentinel Reporting**
