## 2026-08-29T04:16:38Z
You are Worker M1: Database Schema, Migrations & Aggregation Backend Implementer.

Authoritative Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Scope Document: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Your Agent Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusively Owned Files:
- `backend/migrations/001_disease_scans_and_outbreak_alerts.sql`
- `backend/schema.sql`
- `backend/supabase_setup.sql`
- `app/src/main/java/com/example/model/DiseaseScanModels.kt`
- `app/src/main/java/com/example/DiseaseAggregationService.kt`
- `app/src/main/java/com/example/SupabaseClient.kt`

Your Instructions:
1. Implement the complete PostgreSQL migration `backend/migrations/001_disease_scans_and_outbreak_alerts.sql` and update `backend/schema.sql` and `backend/supabase_setup.sql`:
   - `public.disease_scans` table (UUID, disease_name, crop_name, state, district, latitude, longitude, severity, confidence, scanned_at).
   - `public.state_adjacencies` table with full symmetric adjacency graph for Indian states.
   - `public.outbreak_alerts` table (id, disease_name, source_state, target_state, alert_type: EPICENTER/EARLY_WARNING, severity, scan_count, threshold_density, time_window_hours, message, recommended_action, predicted_market_impact_pct, is_active, timestamps).
   - Indices and RLS policies.
   - Trigger Function `fn_evaluate_disease_outbreak()` executing scan count >= 100 in rolling 7 days (168 hours), generating/updating EPICENTER alert for the source state and fanning out EARLY_WARNING alerts for all adjacent neighboring states.
2. Implement Kotlin data models in `app/src/main/java/com/example/model/DiseaseScanModels.kt`:
   - `DiseaseScanPayload`, `DiseaseScanRecord`, `OutbreakAlertRecord`, and enums.
3. Implement `app/src/main/java/com/example/DiseaseAggregationService.kt`:
   - `recordScan()`: Async PostgREST POST to `/rest/v1/disease_scans`.
   - `fetchActiveAlerts(state)`: PostgREST GET from `/rest/v1/outbreak_alerts?target_state=eq.{state}&is_active=eq.true`.
   - `StateAdjacencyGraph`: Full in-memory adjacency map of Indian states for zero-latency local lookups.
   - `evaluateDensityThreshold(scans: List<DiseaseScanRecord>, threshold: Int = 100, windowHours: Long = 168): List<OutbreakAlertRecord>`: Pure evaluation function that calculates density and generates Epicenter & Neighbor Early Warning alerts.
4. Update `app/src/main/java/com/example/SupabaseClient.kt`:
   - Add `recordDiseaseScan` and `fetchOutbreakAlerts` helper methods in `SupabaseApi`.
5. Run `./gradlew assembleDebug` to verify Kotlin code compiles cleanly.
6. Write full completion report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1\handoff.md` and send message when done.
