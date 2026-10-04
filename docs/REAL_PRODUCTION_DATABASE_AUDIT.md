# NuKropAI — Real Production Database Audit & Migration Architecture

**Document Version:** 1.0.0  
**Audit Date:** October 3, 2026  
**Auditor:** Antigravity AI Engineering Architecture Team  
**Scope:** Complete Supabase Schema, Security Policies (RLS), Realtime Publications, Stored Procedures, and API Client Query Alignment  
**Compliance Standards:** Digital Personal Data Protection (DPDP) Act 2023, Zero Data Leakage, Honest Provenance Tracking  

---

## 1. Executive Summary & Audit Mandate

NuKropAI is transitioning from prototype/demo seed scripts to an enterprise-grade, production-hardened agrarian intelligence backend powered **exclusively by Supabase** (PostgreSQL, Supabase Auth, Realtime Engine, Supabase Storage, and Edge Functions). 

This audit was initiated under strict non-negotiable mandates:
1. **Zero UI Redesign / Zero Drift:** The existing Android & Web frontend (`app/src/main/assets/index.html` and `nukrop_emulator.html`) represents the absolute, verified product. Backend queries must match existing UI models without altering visual flows.
2. **Zero Firebase:** No Firebase components, SDKs, or services. Supabase is the sole backend.
3. **Zero Fabricated / Seed Data in Production:** All hardcoded drivers (`GH-4192 Suresh Yadav`, `GH-5521 M. Venkatesh`, `GH-3104 K. Anjaiah`), hardcoded mandi prices, simulated outbreak counts (`142`, `12.5%`), and fake community personas (`రాజేశ్వర్ రావు`, `డా. పి. శ్రీనివాస్`) are eliminated from production paths and isolated into a dedicated `supabase/seed/demo_data.sql`.
4. **Honest Government Data Provenance:** Market data integrated via Open Government Data (OGD) Platform India (`data.gov.in`), Agmarknet, DMI, and e-NAM must never be falsely marked "LIVE" if it represents daily or delayed settlement auctions. Provenance fields (`source_name`, `source_url`, `source_dataset`, `trade_date`, `fetched_at`, `freshness_status`) are strictly required.
5. **Real GPS & Distance Calculation:** Farmer GPS coordinates must dynamically drive nearest-mandi calculations via Haversine / PostGIS RPC functions rather than hardcoding static coordinates.

---

## 2. Comprehensive Inventory of Existing Database Objects

| Table / Object | Primary Key | Foreign Keys | Current RLS Status | Production Deficiency Identified |
|---|---|---|---|---|
| `public.profiles` | `id UUID` (references `auth.users`) | `auth.users(id)` | Inconsistent (`USING (TRUE)` in full schema vs `auth.uid() = id` in early migration) | Contained dangerous hardcoded default locations (`Warangal`, `Geesugonda`, `2.50 acres`). |
| `public.user_profiles` | `id UUID` | None | `USING (TRUE)` permissive | Permissive access allowed any client to read/write all farmer identities. |
| `public.disease_scans` | `id UUID` | `user_id -> profiles(id)` | `USING (TRUE)` permissive | Permissive RLS exposed private farmer diagnostic images and GPS coordinates. |
| `public.outbreak_alerts` | `id UUID` | None | Public read | Contained static fake outbreak seed records (`scan_count: 142`). Write access was not restricted to service roles. |
| `public.community_posts` | `id UUID` | `author_id -> profiles(id)` | Permissive write | Allowed spoofing of author IDs and unauthenticated insertions. Seed records contained fake personas. |
| `public.community_comments` | `id UUID` | `post_id -> community_posts(id)` | Permissive write | Lacked author ownership enforcement on inserts and edits. |
| `public.community_likes` | `id UUID` | `post_id -> community_posts(id)` | Permissive write | Lacked unique constraint on `(post_id, user_id)` in older scripts, risking vote manipulation. |
| `public.haul_bookings` | `id VARCHAR(50)` | None | `USING (TRUE)` permissive | Permissive read/write exposed farmer phone numbers, load volumes, and pickup coordinates to competitors. |
| `public.driver_telemetry` | `id UUID` | None | Permissive read & write | Hardcoded 3 fake drivers. Anyone could update driver coordinates. Offline drivers remained perpetually visible. |
| `public.peer_messages` | `id UUID` | None | `USING (TRUE)` permissive | Lacked participant isolation; anyone could inspect private direct chat between farmers and drivers. |
| `public.mandi_live_rates` | `id UUID` | None | `USING (TRUE)` permissive | Missing government provenance columns (`source_name`, `source_url`, `trade_date`, `freshness_status`). |
| `public.mandi_ingestion_runs` | *NEW TABLE* | None | Service role only | Did not exist previously; audit run tracking was missing. |
| `public.price_alerts` | `id UUID` | `user_id -> profiles(id)` | Private (`auth.uid() = user_id`) | Needs index on `(user_id, crop_slug)`. |
| `public.khata_transactions` | `id UUID` | `user_id -> profiles(id)` | Private (`auth.uid() = user_id`) | Needs date and type indexes for fast ledger aggregation. |
| `public.machinery_listings` | `id UUID` | `owner_id -> profiles(id)` | Permissive | Owner verification missing on update/delete; needs public read only for `is_available = TRUE`. |
| `public.machinery_bookings` | `id UUID` | `machinery_id`, `user_id` | Permissive | User isolation missing; anyone could inspect equipment booking schedules. |

---

## 3. Analysis of Existing Client Supabase Queries (`supabase_integration.js` & `index.html`)

An exhaustive scan of `app/src/main/assets/index.html` and `app/src/main/assets/js/supabase_integration.js` revealed:
1. **Mandi Rates Query:**
   - Client calls `fetch(`${SUPABASE_CONFIG.url}/rest/v1/mandi_live_rates?select=*`)` at line 7536 in `index.html`.
   - Client also provides `nk_fetchMandiRates(state, limit)` in `supabase_integration.js`.
   - **Remediation:** Must keep backward compatibility with `select=*` on `mandi_live_rates` while introducing `nk_fetchNearbyMandis(lat, lng, radiusKm, commodity)` calling RPC `get_nearby_mandis` for spatial proximity matching.
2. **Driver Telemetry & Presence:**
   - Realtime channel `gps:${driverId}` tracks presence and broadcasts GPS updates every 3 seconds.
   - In `driver_telemetry`, records with `is_online = true` were queried without checking `last_ping`. If a driver app crashes, `is_online` remained `true` indefinitely.
   - **Remediation:** RLS policy on `driver_telemetry` must restrict public SELECT to `is_online = TRUE AND last_ping > NOW() - INTERVAL '5 minutes'`.
3. **Profile Creation Defaults:**
   - `nk_signUp()` creates records in `profiles` and `user_profiles`.
   - Previous schema defaulted `state` to `'Telangana'`, `district` to `'Warangal'`, `village` to `'Geesugonda'`, and `land_extent_acres` to `2.50`.
   - **Remediation:** Alter column defaults to `NULL`. Farmer location and land extent must be supplied by the user or reverse-geocoded from permitted device GPS.

---

## 4. Production Row-Level Security (RLS) Remediation Matrix

All tables now have `ROW LEVEL SECURITY` enabled with granular, principle-of-least-privilege policies:

```
┌──────────────────────────────┬──────────────────┬────────────────────────────────────────────────────────┐
│ Table                        │ Command          │ Policy Condition                                       │
├──────────────────────────────┼──────────────────┼────────────────────────────────────────────────────────┤
│ profiles                     │ SELECT / UPDATE  │ auth.uid() = id                                        │
│ disease_scans                │ ALL              │ auth.uid() = user_id                                   │
│ khata_transactions           │ ALL              │ auth.uid() = user_id                                   │
│ peer_messages                │ SELECT           │ auth.jwt()->>'email' IN (sender_email, receiver_email) │
│ peer_messages                │ INSERT           │ auth.jwt()->>'email' = sender_email                    │
│ haul_bookings                │ SELECT           │ auth.uid()::text = farmer_id OR                        │
│                              │                  │ auth.uid()::text = driver_id OR                        │
│                              │                  │ (driver_id IS NULL AND status = 'PENDING')             │
│ haul_bookings                │ INSERT           │ auth.uid()::text = farmer_id                           │
│ driver_telemetry             │ SELECT           │ is_online = TRUE AND last_ping > NOW() - '5 min'::INT  │
│ driver_telemetry             │ INSERT / UPDATE  │ auth.uid()::text = driver_id                           │
│ mandi_live_rates             │ SELECT           │ TRUE (Public open access)                              │
│ mandi_live_rates             │ INSERT / UPDATE  │ auth.role() = 'service_role'                           │
│ mandi_ingestion_runs         │ SELECT / ALL     │ auth.role() = 'service_role'                           │
│ outbreak_alerts              │ SELECT           │ is_active = TRUE                                       │
│ outbreak_alerts              │ INSERT / UPDATE  │ auth.role() = 'service_role'                           │
└──────────────────────────────┴──────────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. Real Government Mandi Data Architecture

### 5.1 Official Source Identification
- **Catalog Portal:** Open Government Data (OGD) Platform India (`data.gov.in`).
- **Publishing Authority:** Directorate of Marketing & Inspection (DMI), Ministry of Agriculture & Farmers Welfare, Government of India.
- **Dataset Title:** Current Daily Price of Various Commodities from Agricultural Produce Market Committees (APMCs).
- **Update Cadence:** Once daily following APMC electronic market session reconciliation (typically 17:00–21:00 IST).

### 5.2 Provenance Data Schema
Every row in `public.mandi_live_rates` now encapsulates immutable audit trails:
- `source_name`: `'Directorate of Marketing & Inspection (DMI), Ministry of Agriculture & Farmers Welfare via data.gov.in'`
- `source_url`: `'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'`
- `source_dataset`: `'Daily APMC Mandi Market Prices'`
- `trade_date`: Official transaction date recorded by the APMC secretary.
- `fetched_at`: System ingestion timestamp.
- `freshness_status`: Dynamic classification (`DAILY` for current date, `RECENT` for ≤ 3 days, `DELAYED` for > 3 days).

### 5.3 Ingestion Pipeline Tracking (`mandi_ingestion_runs`)
Every invocation of the ingestion pipeline logs its telemetry to `public.mandi_ingestion_runs` with:
- Total records received from upstream API.
- Records inserted / updated.
- Records rejected due to validation failure (e.g., negative prices, missing commodity name).
- Execution timing and error diagnostics.

---

## 6. Migration Execution Plan

1. **Step 1: Demo Seed Isolation**
   - Create `supabase/seed/demo_data.sql` holding static test records for local developer testing.
2. **Step 2: Database Schema & RLS Hardening**
   - Author `supabase/migrations/20261003010000_production_mandi_and_rls.sql` providing:
     - Nullification of default profile coordinates.
     - Mandi provenance columns and unique natural keys.
     - `mandi_ingestion_runs` table.
     - Haversine `get_nearby_mandis()` stored procedure.
     - Strict, ownership-bound RLS policies.
   - Update `supabase/FULL_NUKROPAI_SCHEMA.sql` to serve as the unified, production-clean reference for Supabase SQL Editor execution.
3. **Step 3: Edge Function Implementation**
   - Author `supabase/functions/mandi-sync/index.ts` to ingest and validate government data feeds with full provenance tracking.
4. **Step 4: Client Integration Alignment**
   - Update `supabase_integration.js` to support `nk_fetchNearbyMandis` with real farmer GPS.
   - Update `index.html` to reflect honest freshness badges and real online driver queries.
5. **Step 5: Verification & Verification Report**
   - Author `docs/REAL_GOVERNMENT_MANDI_DATA_VERIFICATION.md`.
   - Run JS syntax audits and complete Android Gradle verification.
