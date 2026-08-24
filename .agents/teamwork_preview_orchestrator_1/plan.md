# Execution Plan — NuKropAI Android App Audit & Fixes

## Phase 0: Survey & Discovery
1. Spawn 3 specialized Explorers in parallel:
   - Explorer 1 (UI Alignment Specialist): Investigate all Jetpack Compose screens (Home, Market, Profile, Scanner, Loan, etc.), bottom navigation bar insets, list bottom padding, text overflow, layout clipping.
   - Explorer 2 (Kotlin Bug Hunter): Investigate codebase for crashes, unhandled nullability, coroutine leaks, infinite loading states, error handling in ViewModels/Repositories.
   - Explorer 3 (API & Connection Specialist): Inspect Groq AI, Supabase DB, Agmarknet API configurations, auth tokens, interceptors, network request endpoints, rate-limiting & error recovery logic.

## Phase 1: Synthesis & PROJECT.md
1. Aggregate survey reports into Feature Inventory and Defect Catalog.
2. Define interface contracts, file ownership, and milestone breakdown in `PROJECT.md`.
3. Establish verification criteria and test commands.

## Phase 2: Milestone Execution (Worker -> Reviewer -> Challenger -> Auditor)
1. Milestone R1: UI Alignment, Polish & Bottom Padding.
2. Milestone R2: Bug Squashing, Crash Fixes & Robust State Handling.
3. Milestone R3: API Token Validation, Connection Verification & Network Error Handling.

## Phase 3: Acceptance & Build Verification
1. Test compilation via `./gradlew assembleDebug` or equivalent gradle build tasks executed by workers.
2. Independent review by Reviewers & Challengers.
3. Integrity Forensics by Auditor.

## Phase 4: Final Synthesis & Parent Notification
1. Complete handoff report.
2. Notify parent sentinel.
