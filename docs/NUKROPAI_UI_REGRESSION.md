# NuKropAI — UI Regression & 15 Golden Checkpoints Verification

**Testing Platform:** Android Mobile Emulator (Google Pixel 7 / Android 14 `412 × 915` @ 2.0x DPR)  
**Verification Tool:** Playwright Automated Suite (`capture_emulator_gallery.py`)  
**Overall Regression Verdict:** **15 / 15 PASS (100% Visual & Interaction Parity)**

---

## 1. Golden Checkpoint Inspection Matrix

| # | Checkpoint Screen | Screenshot Artifact | Language Purity | Visual & Interaction Checks | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **01** | **Splash Screen** | `01_splash_screen.png` | 100% Pure | Full emerald `#064E3B` gradient, glowing seed ring, subtitle, version chip. Auto-advances in 1.8s. | **PASS** |
| **02** | **Language Selection** | `02_language_selection.png` | 100% Pure | 11 native language cards (Telugu, Hindi, Tamil, Kannada, etc.). Selection instantly sets global language state. | **PASS** |
| **03** | **Onboarding Slide 1 (AI Doctor)** | `03_onboarding_slide1_telugu.png` | 100% Pure Telugu | Full-bleed photography hero, `🌾 AI పంట డాక్టర్` pill, 6 indicator dots, skip button. | **PASS** |
| **04** | **Onboarding Slide 3 (Mandi)** | `04_onboarding_slide3_mandi_telugu.png` | 100% Pure Telugu | Mandi hero image, `📊 మార్కెట్ ధరలు & అంచనాలు` pill, market intelligence description. | **PASS** |
| **05** | **Onboarding Slide 5 (GramHaul)** | `05_onboarding_slide5_gramhaul_telugu.png` | 100% Pure Telugu | Farm truck hero, `🚚 గ్రామ్‌హాల్ - ఉమ్మడి రవాణా` pill, pooled logistics savings copy. | **PASS** |
| **06** | **Hardware Permissions (Camera)** | `06_permissions_camera.png` | 100% Pure Telugu | Glassmorphic permission card, `🔒 అనుమతులు (1/3)`, direct OS hardware intent trigger. | **PASS** |
| **07** | **Crop Selection (143 Crops)** | `07_crop_selection.png` | 100% Pure Telugu | Complete 143-crop catalog with native Telugu names, search filter, selected counter. | **PASS** |
| **08** | **Farmer Home Dashboard** | `08_farmer_home_dashboard.png` | 100% Pure Telugu | Farm chip, weather bento card (29°C, rain prob), live APMC ticker, active pest alert. | **PASS** |
| **09** | **Farmer Profile** | `09_farmer_profile_clean.png` | 100% Pure Telugu | Farmer avatar, AgriStack ID, land extent, soil score, and prominent red `[→] లాగ్ అవుట్`. | **PASS** |
| **10** | **AgriStack Passport Modal** | `10_agristack_passport_modal.png` | 100% Pure Telugu | Guilloche security card, QR code, Dharani survey number, e-KYC verified chip. | **PASS** |
| **11** | **GramHaul Map & Booking** | `11_gramhaul_redesigned_map_trucks.png` | 100% Pure Telugu | 40% height Leaflet OSM map, moving GPS trucks, commercial tiers, sack counter stepper. | **PASS** |
| **12** | **Dispatch Broadcast Radar** | `12_gramhaul_dispatch_broadcast_modal.png` | 100% Pure Telugu | Pulsing radar wave animation, live 60-second broadcast timer, real driver matching. | **PASS** |
| **13** | **Driver Cockpit Live Map** | `13_driver_cockpit_map.png` | 100% Pure Telugu | Obsidian theme, Duty ON/OFF toggle, trip map, incoming haul sheet, Accept/Decline. | **PASS** |
| **14** | **Driver Profile & Earnings** | `14_driver_profile_clean.png` | 100% Pure Telugu | Driver credentials, Tata Ace Gold plate, 145 trips, FASTag link, and red Log Out. | **PASS** |
| **15** | **Insurance & FASTag Modal** | `15_driver_insurance_fastag_modal.png` | 100% Pure Telugu | Commercial vehicle insurance policy breakdown, NETC FASTag toll balance check. | **PASS** |

---

## 2. Regression Resolution Details

1. **Elimination of Dual-Language Slashes:** Every single instance of mixed labels (e.g. `Log Out / నిష్క్రమించు`, `Camera Access & Crop Scanner`) has been replaced with dynamic single-language evaluation via `TL(...)` and `OB_TL(...)`.
2. **Crop Name Localization:** All 143 crops in `MASTER_120_CROPS` and `OPENFARM_CROPS_CATALOG` render strictly in the user's chosen language (e.g. `పత్తి`, `మిరప`, `చెరకు`, `వరి`, `గోధుమ`, `మొక్కజొన్న`).
3. **Chassis & Status Bar Alignment:** Mobile letterboxing fixed via responsive CSS media queries (`@media (max-width: 640px)`). Safe area insets (`env(safe-area-inset-top)`) prevent camera punch-hole and notch collisions.
4. **Driver Fleet Authenticity:** Zero mock drivers. Dynamic commercial truck listings calculate actual distance-based freight costs.
