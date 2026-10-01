# Dispatch: Worker M1 (Real GramHaul Map & Supabase Backend Integration)
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1
Original Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Survey Report: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_1_gen2\handoff.md
Project Index: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Objective: Implement Milestone 1 (R1)
1. **Remove Fake SVG Map**:
   - In `nukrop_emulator.html` and `app/src/main/assets/index.html`, locate `APP_VIEWS.gramhaul()` and remove `#gramhaul-radar-svg` (lines ~11216-11280) which covers the map with a fake dark vector drawing.
2. **Implement Interactive Leaflet.js Map**:
   - In `initGramhaulOpenStreetMap(lat, lng)`, initialize Leaflet on container `'gramhaul-osm-map'`.
   - Ensure the map centers dynamically on the user's coordinates (from GPS `currentGeoPosition.lat, currentGeoPosition.lng`).
   - Add OpenStreetMap / CARTO Positron tile layer (`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` or CARTO Voyager).
   - Add custom farm marker for user location with pulsating ring icon.
   - Wire `openScreen('gramhaul')` to trigger `setTimeout(initGramhaulOpenStreetMap, 100)` and call `gramhaulMapInstance.invalidateSize()`.
3. **Supabase `public.truck_listings` Backend Integration**:
   - Create SQL migration `backend/migrations/003_gramhaul_truck_listings.sql` with full table definition (`id`, `user_id`, `driver_name`, `driver_phone`, `vehicle_type`, `vehicle_plate`, `capacity_tons`, `total_bags_capacity`, `filled_bags`, `rate_per_bag`, `solo_rate`, `origin_village`, `destination_mandi`, `departure_time`, `latitude`, `longitude`, `status`, `rating`, `trips_count`, `created_at`), indexes, RLS policies, and seed data.
   - In JavaScript, implement `fetchGramhaulTrucks()`:
     - Fetches listings from `${SUPABASE_CONFIG.url}/rest/v1/truck_listings?status=eq.ACTIVE&order=created_at.desc`.
     - Plots dynamic Leaflet markers for each truck with custom icon (vehicle emoji + price pill) and popup with "Book Pooled Slot".
     - Renders real truck listing cards in `#gramhaul-trucks-container`.
     - Includes a clean fallback to local seed data if network/Supabase returns 404/offline, but ALWAYS attempts real PostgREST first.
   - In `submitDriverTruckListing()`:
     - Persists new truck listing to Supabase via `POST ${SUPABASE_CONFIG.url}/rest/v1/truck_listings`.
     - On response, dynamically adds new truck marker to Leaflet map, prepends to list, and shows luxury toast confirmation.
4. **User Location Centering**:
   - In `refreshGramhaulLocation()`:
     - Uses `navigator.geolocation.getCurrentPosition()`.
     - Saves coordinates to `localStorage` (`nukrop_lat`, `nukrop_lon`, `nukrop_city`).
     - Smoothly flies map to new coordinates: `gramhaulMapInstance.flyTo([lat, lng], 13)`.
     - Updates farm marker position and HUD text.
5. **Maintain Dual-File Parity**:
   - Ensure all changes are applied to both `nukrop_emulator.html` and `app/src/main/assets/index.html`.
6. **Automated Verification**:
   - Run existing test suite (`node test_production_readiness.js`) and ensure no regressions.
   - Write/run automated verification script to prove Leaflet map initialization, truck fetching, and truck addition.
7. **Write Handoff Report**:
   - Write report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1\handoff.md`.
   - Send completion message to parent with path and test output.

## 2026-09-09T08:43:13Z
You are Worker M1 (teamwork_preview_worker).
Your working directory is: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1
Read your dispatch at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1\DISPATCH.md
Read the original request at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Read the survey report at: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_1_gen2\handoff.md
Read the project scope at: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Mission:
Implement Milestone 1: Real GramHaul Leaflet Map & Supabase Truck Listings.
1. Remove the fake SVG radar `#gramhaul-radar-svg` in `nukrop_emulator.html` and `app/src/main/assets/index.html`.
2. Ensure Leaflet interactive map mounts cleanly onto `#gramhaul-osm-map`, centers dynamically on the user's real GPS coordinates, plots custom farm and truck markers, and binds popups.
3. Wire `openScreen('gramhaul')` to initialize the map and invalidate size.
4. Create the SQL migration `backend/migrations/003_gramhaul_truck_listings.sql` with full table definition, RLS, indexes, and seed records.
5. Implement `fetchGramhaulTrucks()` and `submitDriverTruckListing()` with live PostgREST integration to Supabase `truck_listings` table.
6. Support user GPS refresh in `refreshGramhaulLocation()` and centering via `flyTo([lat, lng], 13)`.
7. Maintain exact parity between `nukrop_emulator.html` and `app/src/main/assets/index.html`.
8. Run tests with `node test_production_readiness.js` and verify zero regressions.
9. Write your detailed handoff report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1\handoff.md`.
10. Send a message to parent with the handoff path and verification results.
