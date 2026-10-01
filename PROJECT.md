# Project: NuKropAI Integration, Hardening & UI Polish

## Architecture
- **Platform**: Web/Desktop/PWA Emulator (`nukrop_emulator.html`) + Android WebView runtime (`app/src/main/assets/index.html`) + Supabase Cloud Backend (`https://yxjqseiegwjdfnccdchk.supabase.co`) + Android Kotlin Native Engine (`app/src/main/java/com/example/`).
- **Core Design**:
  - Modular View Architecture with 16 distinct OS views managed in `window.APP_VIEWS`.
  - Real-time Geospatial Layer powered by Leaflet.js (v1.9.4) and OpenStreetMap / CARTO Positron tiles.
  - Supabase REST API (PostgREST) + Realtime WebSocket synchronization for community and logistics.
  - Multi-tier Fallback Resiliency: Hardware GPS -> Nominatim Reverse Geocoding -> AgriStack Profile -> State Selector -> National Overview (Zero Hardcoded Location Fallbacks).
  - Airbnb / PayPal Design System: Centralized CSS tokens, multi-layered elevation shadows, 8pt spatial grid, tactile micro-animations, and shimmer skeleton loaders across all asynchronous surfaces.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Real GramHaul Leaflet Map | Replace fake SVG radar with Leaflet.js map centered on user GPS coordinates with custom truck/farm markers and popup booking | M1 | Survey R1 [DONE] |
| 2 | Supabase Truck Listings CRUD | Full backend integration to add new truck listings, fetch active listings, and delete/manage own listings | M1 | Survey R1 [DONE] |
| 3 | Dynamic Pest & Disease Alerts | Remove all hardcoded "Warangal" fallbacks; dynamically filter and fetch alerts based on user's detected state and district | M2 | Survey R2 [DONE] |
| 4 | Resilient Geolocation Hierarchy | Multi-tier state resolution (GPS -> Profile -> State Selector -> National Overview) with zero synthetic location fallbacks | M2 | Survey R2 [DONE] |
| 5 | Community Follow / Unfollow | Real user following/unfollowing mechanism linked to Supabase `user_follows` and reflected on profile stats | M3 | Survey R3 [DONE] |
| 6 | Community Real Likes with Sync | Real like/unlike toggle with atomic database counter sync in Supabase `post_likes` and optimistic UI updates | M3 | Survey R3 [DONE] |
| 7 | Edit & Delete Own Community Posts | Post ownership verification (`post.user_id == current_user.id`) with full edit modal and delete confirmation wired to Supabase | M3 | Survey R3 [DONE] |
| 8 | Airbnb/PayPal-Grade Design Polish | Standardized typography, elevation shadows, 8pt spacing grid, borders, and micro-animations across all 16 views | M4 | Survey R4 |
| 9 | Universal Shimmer Skeleton Loaders | Pure CSS shimmer loaders on all 6 async surfaces: Leaflet map, trucks, community feed, mandi rates, weather, and bioshield alerts | M4 | Survey R4 |
| 10 | 5-Tier Automated E2E Test Suite | Automated test harness executing Tier 0 to Tier 4 tests verifying R1, R2, R3, and R4 with 100% pass rate | M5 | Survey Acceptance |
| 11 | Independent Forensic Integrity Audit | Systematic audit verifying zero dummy placeholders, zero synthetic cheating, and full functional integrity | M5 | Survey Acceptance |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Real GramHaul Map & Backend Integration | Leaflet map initialization, remove fake SVG, Supabase `truck_listings` schema/CRUD, user GPS centering | none | DONE |
| M2 | Dynamic Pest & Disease Alerts | Purge hardcoded "Warangal" strings, implement dynamic state-based alert engine, wire to GPS geocoding | M1 | DONE |
| M3 | Interactive Community Features | Followers/following, real likes, post ownership authorization, edit and delete own posts with Supabase | M2 | DONE |
| M4 | Airbnb/PayPal UI Polish & Skeletons | CSS design tokens, typography, shadows, micro-animations, skeleton loaders across all 6 async surfaces | M3 | IN_PROGRESS |
| M5 | Final E2E Test Verification & Forensic Audit | Run 5-tier test suite, verify 100% test pass, independent review, challenger stress-testing, forensic integrity audit | M1, M2, M3, M4 | PLANNED |

## Interface Contracts
### Leaflet ↔ GramHaul Truck Listings
- `initGramhaulOpenStreetMap(userLat, userLng)`: Mounts Leaflet map onto `#gramhaul-osm-map`, removes `#gramhaul-radar-svg`, plots user farm marker at `[lat, lng]` and dynamic truck markers from Supabase.
- `fetchGramhaulTrucks(userLat, userLng)`: Queries `${SUPABASE_CONFIG.url}/rest/v1/truck_listings?status=eq.ACTIVE` and populates map markers and `#gramhaul-trucks-container`.
- `submitDriverTruckListing(formData)`: Dispatches `POST ${SUPABASE_CONFIG.url}/rest/v1/truck_listings` and updates both map and feed.

### LocationEngine ↔ Dynamic Pest Alerts
- `getEffectiveUserState()`: Returns state string from GPS/Nominatim, profile, or search state. Never defaults to "Warangal".
- `getEffectiveUserDistrict()`: Returns district string from GPS/Nominatim, profile, or search. Never defaults to "Warangal".
- `fetchDynamicPestAlerts(state, district)`: Queries Supabase `outbreak_alerts` or evaluates `getRegionalPestMatrix(state, district)`, updating BioShield radar cards and home news ticker dynamically.

### Community Hub ↔ Supabase PostgREST
- `getCurrentUserId()`: Returns persistent farmer user ID.
- `toggleCommunityLike(postId)`: Dispatches `POST/DELETE` to `/rest/v1/post_likes` and optimistically updates heart icon and counter.
- `toggleFollowUser(authorId)`: Dispatches `POST/DELETE` to `/rest/v1/user_follows` and updates follower counts on UI and profile.
- `saveEditedCommunityPost(postId, title, content, crop)`: Dispatches `PATCH /rest/v1/community_posts?id=eq.${postId}&user_id=eq.${currentUserId}`.
- `deleteCommunityPost(postId)`: Dispatches `DELETE /rest/v1/community_posts?id=eq.${postId}&user_id=eq.${currentUserId}`.

## Code Layout
- `nukrop_emulator.html`: Primary web application emulator containing all 16 views, styling, and JavaScript logic.
- `app/src/main/assets/index.html`: Android embedded WebView asset maintained in exact parity with `nukrop_emulator.html`.
- `backend/migrations/`: SQL migration files for Supabase database schema.
  - `003_gramhaul_truck_listings.sql`: Schema for `truck_listings`.
  - `004_community_interactive.sql`: Schema for `post_likes`, `user_follows`, `community_posts.user_id`, and triggers.
- `tests/`: Automated test runner and test cases.
  - `test_harness.js`: Core assertion runner.
  - `test_production_readiness.js`: Master 5-tier test suite.
  - `verify_milestone1_gramhaul.js`: M1 verification suite.
  - `verify_milestone2_pest_alerts.js`: M2 verification suite.
  - `verify_milestone3_community.js`: M3 verification suite.
  - `verify_milestone4_ui_polish.js`: M4 verification suite.
