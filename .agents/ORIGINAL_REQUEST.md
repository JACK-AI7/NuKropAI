# Original User Request

## Initial Request — 2026-09-01T04:29:46Z

# Teamwork Project Prompt — Final

> Status: Launched
> Goal: Execute teamwork_preview
> Requested team: Full multi-agent team (Builders, Auditors, Testers)

A fullstack production-grade Agrarian Intelligence OS (NuKropAI) audit and hardening sweep: line-by-line verification, real-time live data feeds (Agmarknet Mandi rates, live weather radar, Supabase backend, AgriStack RoR, ONNX/TensorFlow crop disease ML inference, GramHaul fleet tracking, and ICAR bio-calculators), complete toolchain health, zero mock regressions, and strict automated test verification.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: development

## Requirements

### R1. Fullstack Architecture & Live Data Pipeline Verification
Audit the entire NuKropAI codebase line-by-line across frontend emulator (
ukrop_emulator.html), Android Kotlin core, and Supabase backend. Verify that live external APIs (Agmarknet APMC mandi prices, live weather sensor windows, Supabase cloud sync, OpenFarm crop database, and AgriStack land registry records) operate with resilient live error-handling, proper fallbacks, and zero synthetic dummy placeholders.

### R2. Complete Feature & Toolchain Health Sweep
Verify end-to-end functionality for all 16 OS views and tools:
- **Home & Live Micro-Weather**: Real-time 3-hour spray window calculation, astronomical solar cycle, and crop carousel.
- **AI Crop & Soil Scanner**: Groq Vision & on-device leaf/soil disease diagnostic inference pipeline.
- **Mandi Market Engine**: Agmarknet price modal rates, 7-day trend analysis, and price threshold alert triggers.
- **GramHaul Logistics Fleet**: Live GPS radar, driver pooling calculator, and freight quote engine.
- **AgriStack & KCC Finance**: Digital RoR passport, cadastral geo-fenced land plots, Soil Health Card (SHC), and pre-approved KCC loan disbursal.
- **BioRx Pharmacy & Calculators**: ICAR NPK fertilizer calculator, pesticide tank dosage, farm budget ROI, and indigenous bio-formulations.
- **Kisan Community Hub**: Multilingual Q&A feed, audio TTS voice note player, photo/video media attachments, and agronomist verification.

### R3. Internationalization (i18n) & Visual Polish Integrity
Ensure 100% clean rendering and strictly single-language dropdowns across all 11 supported Indian languages (Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, English) with zero text truncation, zero duplicate cards, and Apple/Airbnb-grade aesthetic polish.

## Acceptance Criteria

### Automated Test Suite & Logic
- [ ] Automated end-to-end test suite passes 100% across all 176 views (16 screens × 11 languages).
- [ ] Real-time spray advisory calculator accurately maps current hour to continuous 3-hour windows.
- [ ] Strictly single-language crop selector verified with 0 mixed-script occurrences.
- [ ] Android build check: ./gradlew assembleDebug exits with code 0 (if Android workspace is active).

### Independent Auditor Review
- [ ] Independent auditor confirms zero broken tool links, zero hardcoded crash bugs, and complete DPDP Act 2023 privacy compliance.

## Follow-up — 2026-09-04T07:47:29Z

# Teamwork Project Prompt — Final

> Status: Launched
> Goal: Execute teamwork_preview
> Requested team: Full multi-agent team (Builders, Auditors, Testers)

We are upgrading the NuKropAI Agrarian OS to a production-ready state. This includes integrating live Supabase authentication, connecting the AI Crop Scanner to the Gemini Vision API, implementing a real Community feed, and fetching live Agmarknet market data.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: benchmark

## Requirements

### R1. Live Supabase Authentication
Implement real Supabase authentication for Sign Up, Email Login, and Google Login. Ensure the user's session, name, and profile are remembered persistently across app restarts. 

### R2. Gemini Vision AI Integration
Connect the AI Crop & Soil Scanner to the Gemini Vision API (using local environment variables for the API key) to process camera/gallery uploads and return real diagnostic results.

### R3. Community Media Feed
Upgrade the Kisan Community section to fully support rendering real uploaded images and videos in the feed, moving away from static mock text.

### R4. Real Agmarknet Market Data
Replace mock Mandi rates with real live daily prices fetched directly from the Agmarknet/Gov API (or a suitable wrapper) based on the user's location.

## Acceptance Criteria

### Authentication
- [ ] User can successfully log in with Email/Password or Google via Supabase.
- [ ] Restarting the app automatically logs the user back in without prompting for credentials.
- [ ] User's name is displayed correctly in the app header/profile.

### AI Scanner
- [ ] Uploading an image to the scanner successfully hits the Gemini Vision API and returns a parsed diagnostic response in the UI.

### Community Media
- [ ] Community feed items containing images or videos render correctly and smoothly in the WebView.

### Live Data
- [ ] The app successfully fetches and displays real-time or daily Mandi rates.

## Follow-up — 2026-09-09T06:07:57Z

# Teamwork Project Prompt — Final

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full agent team

Complete the integration and UI polish of the NuKropAI agriculture app. Replace fake data with real integrations (GramHaul map, Pest Alerts, Community features) and polish the existing UI across all screens to a premium standard (Airbnb/PayPal level).

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: benchmark

## Requirements

### R1. Real GramHaul Map & Backend Integration
Replace the fake SVG map and fake truck data in the GramHaul view with a real interactive map using Leaflet.js. Implement full Supabase backend integration so users can add, view, and manage their own real truck listings based on their actual location.

### R2. Dynamic Pest and Disease Alerts
Update the pest and disease alerts section to fetch and display real-time alerts based on the user's detected state/location, removing any hardcoded fallbacks like "Warangal".

### R3. Interactive Community Features
Enhance the Community tab to support real user interactions, including followers, following, real likes, and the ability to edit/delete own posts. Integrate these features fully with the Supabase backend.

### R4. Complete App UI Polish
Polish the existing UI across all screens in the app to achieve a top-tier premium UI/UX (similar to Airbnb or PayPal). Ensure neat alignment, premium typography, loading skeletons, and consistent micro-animations without doing a top-to-bottom redesign of the layout.

## Acceptance Criteria

### GramHaul Map
- [ ] Leaflet.js map renders without errors and centers on the user's real coordinates.
- [ ] Users can successfully add a new truck listing, and it persists in the backend.
- [ ] Real truck listings fetch from the backend and display on the map.

### Pest Alerts
- [ ] Alerts feed dynamically filters or fetches content based on the user's state.
- [ ] No hardcoded location fallbacks are present in the alert fetching logic.

### Community
- [ ] Following/unfollowing a user updates the database and UI count.
- [ ] Liking a post updates the database and UI count.
- [ ] Users can successfully edit and delete their own posts.

### UI Polish
- [ ] All screens (Home, Profile, Community, GramHaul, etc.) have a consistent, premium design language.
- [ ] Skeleton loaders are implemented for all asynchronous data fetching.


## Follow-up — 2026-10-05T16:59:44Z

Comprehensive senior engineering audit and bug elimination across the entire NuKropAI production ecosystem (Android app, emulator, and web portal) to resolve all UI misalignments, broken event bindings, disconnected features, and simulated placeholders, elevating the application to high-end production grade.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Integrity mode: development

## Strict Constraints & Guardrails
- **STRICT NON-DESTRUCTIVE PRESERVATION**: Do NOT delete, drop, or remove any existing application features, screens, tabs, UI components, assets, database configurations, or functional endpoints. All existing modules must remain 100% connected, functional, and intact.
- **PURE REAL-TIME (ZERO SIMULATION)**: Eliminate any fake or mock timer loops, hardcoded static locations, or synthetic bot conversations; all data must be authentic and connected.

## Requirements

### R1. Comprehensive Line-by-Line Code Audit & Error Remediation
Inspect all scripts and stylesheets in app/src/main/assets/index.html and nukrop_emulator.html to eliminate all runtime errors, broken element references, missing event handlers, CSS visual misalignments, and state desynchronizations without breaking or removing any existing functional features.

### R2. Core Feature Integrity & Pure Real-Time Operation
Verify that all application subsystems function in real-time with zero synthetic simulations:
- **Language Selection & Persistence**: Selected language must strictly persist across page reloads and app restarts without defaulting back to Telugu.
- **Plant / Crop Selector**: Item counter must accurately match the exact number of selected plants with zero off-by-one errors.
- **Driver GPS Telemetry & Tracking**: Real physical GPS location updates when duty is turned on, rendering live moving truck pins on the farmer's GramHaul map.
- **Rapido-Style Trip Flow & OTP Verification**: Farmer booking broadcast, driver exclusive trip acceptance, farm arrival notification, 4-digit PIN verification to start the trip (IN_TRANSIT), and destination arrival.
- **Dynamic Driver UPI Settlement**: Authentic driver UPI QR code and payment intent generation for direct farmer-to-driver payments with no hardcoded mock payment IDs.
- **Live Peer-to-Peer Chat**: Instant, bi-directional in-ride messaging between farmer and driver over Supabase Realtime without simulated bot replies.
- **Community Feed & Social Interactions**: Seamless post creation, likes, comments, audio voice notes, and crop filtering with synchronized backend persistence.

### R3. Automated Verification, Clean Build & Release Packaging
Perform automated regression testing on all modified modules, confirm zero JavaScript syntax errors, build the release APK (gradlew assembleRelease), synchronize website download endpoints, and verify full parity between the mobile app and desktop emulator.

## Acceptance Criteria

### Automated Code Quality & Parity
- [ ] Automated syntax and AST checks pass with zero syntax or parse errors for all JavaScript and HTML blocks in app/src/main/assets/index.html and nukrop_emulator.html.
- [ ] Zero unhandled exceptions or missing DOM element reference errors during page startup or screen switching.
- [ ] No existing feature, screen, component, or asset was deleted or disconnected.

### Functional Flow Validation
- [ ] Crop selector UI displays an active count that strictly equals the count of selected crop tags.
- [ ] User language choice remains unchanged after hard reloads and across multi-screen navigation.
- [ ] Driver ON/OFF duty switch activates live GPS broadcast, and the GramHaul map renders live driver coordinates without static simulation coordinates.
- [ ] Trip lifecycle completes end-to-end: Booking -> Driver Acceptance -> Arrival -> 4-Digit OTP Verification -> In-Transit -> Mandi Arrival -> Driver UPI QR Payment.
- [ ] Real in-ride peer-to-peer chat transmits messages reliably in both directions over Supabase Realtime without simulated bot texts.
- [ ] Community like counts, comments list, and new post submissions reflect instantly in the UI and persist in Supabase.

### Build & Delivery
- [ ] Release APK compiles successfully via ./gradlew.bat assembleRelease without packaging errors.
- [ ] Website download assets (web/public/ and web/dist/) are synchronized with the fresh release APK.
