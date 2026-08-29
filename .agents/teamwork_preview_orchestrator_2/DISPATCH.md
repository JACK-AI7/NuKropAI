## 2026-08-29T04:01:09Z

You are the Project Orchestrator for the NuKropAI National Crop Disease Aggregation and Early Warning System.

## Project Scope & Requirements
Authoritative Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md (under timestamp ## 2026-08-29T04:00:33Z)
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Your Agent Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_orchestrator_2

### Requirements
1. **R1. Scan Aggregation & Alert Backend**:
   - Design backend architecture (using Supabase/PostgreSQL schema/migrations, Edge Functions, database triggers, or Kotlin-side aggregation logic) to record anonymous disease scans (disease name, location/state, timestamp).
   - Implement logic counting recent scans. If a specific pest/disease crosses density threshold in a region (e.g. 100 scans in a state), generate an early warning alert for neighboring areas.
   - Include clear database schema/migration scripts for `disease_scans` and `outbreak_alerts`.

2. **R2. Market Impact Calculator**:
   - Implement logic correlating severe regional outbreaks with predicted impact on local mandi prices for that crop.

3. **R3. Android UI Integration**:
   - Update NuKropAI Android app to push scan results to aggregation backend after successful on-device scan.
   - Update Home and/or Market screens (Jetpack Compose) to display active regional outbreak alerts and predicted market price impact.

### Acceptance Criteria
- Clear backend implementation (SQL migration scripts and/or Kotlin logic) for `disease_scans` and `outbreak_alerts`.
- 100 scans in one state must correctly trigger an alert generation (verifiable by independent audit & tests).
- App successfully pushes new scan results.
- UI displays active alerts and price impacts.
- `./gradlew assembleDebug` exits with code 0 (clean compilation, no errors).
