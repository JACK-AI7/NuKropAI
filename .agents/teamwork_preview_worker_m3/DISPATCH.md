## 2026-08-29T04:33:30Z
Worker M3: Android App Scan Hook & Jetpack Compose UI Implementer.

Authoritative Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Scope Document: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Your Agent Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3

Exclusively Owned Files:
- `app/src/main/java/com/example/DiseaseScannerScreen.kt`
- `app/src/main/java/com/example/HomeScreen.kt`
- `app/src/main/java/com/example/MarketScreen.kt`
- `app/src/main/java/com/example/RegionalIntelligenceScreen.kt`
- `app/src/main/java/com/example/AppStrings.kt`

Your Instructions:
1. Update `app/src/main/java/com/example/DiseaseScannerScreen.kt`:
   - In `CameraScanner` / photo picker flow, upon receiving `CropScanData`:
   - If diseased (`data.status != "Healthy"`), push anonymous telemetry via `DiseaseAggregationService.recordScan(payload)` asynchronously on `Dispatchers.IO`. Extract state/district from `LocationHelper.getCurrentLocationStateAndMandi(context)` or `nukrop_farm_profile` SharedPreferences.
   - In `ScanResultView`, add an anonymous privacy badge indicating contribution to the National Outbreak Early Warning Grid.
2. Update `app/src/main/java/com/example/HomeScreen.kt`:
   - Replace the static placeholder pest prediction card with dynamic `RegionalOutbreakAlertSection` fetching active alerts from `DiseaseAggregationService.fetchActiveAlerts(userState)`.
   - Display dynamic outbreak cards with severity color coding, scan density trigger explanation (e.g. ">100 scans in state"), risk level badge, and CTA to view market price impact.
3. Update `app/src/main/java/com/example/MarketScreen.kt`:
   - Insert `OutbreakMarketImpactCard` / `OutbreakPriceImpactBanner` above the 7-day AI forecast card.
   - Correlate searched/selected crop with active alerts using `MarketImpactRepository.calculateImpactForCropAndState(...)`.
   - Render current modal price, predicted peak price, percentage delta (+/- X%), risk level badge, confidence score, impact mechanism, farmer action advisory, and affected mandis list.
4. Update `app/src/main/java/com/example/RegionalIntelligenceScreen.kt` with live outbreak alerts list from `DiseaseAggregationService.fetchAllActiveAlerts()`.
5. Update `app/src/main/java/com/example/AppStrings.kt` with localization strings for outbreak alerts, scan privacy badges, and price impacts.
6. Verify Kotlin compilation by running `./gradlew assembleDebug` using `run_command`.
7. Write completion report in `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m3\handoff.md` and send message when complete.
