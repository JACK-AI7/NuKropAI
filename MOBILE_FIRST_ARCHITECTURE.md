# NuKropAI Mobile-First Architecture — 100% Self-Contained

## Overview
The app now performs **all AI analysis on the device** or via direct cloud API (Gemini). No backend AI processing required. The optional Node.js backend is kept only for user accounts if needed, but scanning works completely offline (except for cloud LLM enhancement and weather).

---

## Components

### 1. On-Device AI (TFLite)
- **Model**: `assets/models/crop_disease_model.tflite` + `crop_disease_labels.txt`
- **Provider**: `OnDeviceAIService`
- **Capabilities**:
  - Classifies crop diseases (48 classes including soil types)
  - Provides basic treatment, prevention tips, and product suggestions (hardcoded)
  - Works 100% offline, instant inference

### 2. Cloud LLM (Gemini Vision) — Optional
- **Service**: Google Gemini 1.5 Flash (free tier)
- **Provider**: `LLMService` using `google_generative_ai` package
- **Role**: Enriches on-device analysis with detailed, context-aware treatment, fertilizer, pesticide advice, and product research.
- **Configuration**: API key saved in Settings → "Gemini API Key"
- **Fallback**: If no key or offline, app uses on-device recommendations only.

### 3. Real-Time Weather
- **Source**: Open-Meteo API (no key required)
- **Fetched**: Directly from mobile, bypassing any backend
- **Data**: Temperature, humidity, wind speed, weather code → translated to condition text and icons
- **Use**: Weather context incorporated into LLM prompts for region- and weather-aware advice

---

## Data Flow (Scan)

```
User captures/selects image
        ↓
ScannerService.scanImage()
        ↓
1. Get GPS location (Geolocator)
2. Fetch weather from Open-Meteo (direct HTTP)
        ↓
3. On-device TFLite inference (fast, offline)
        ↓
4. If Gemini key configured:
   Build prompt with on-device results + weather
   Call Gemini Vision (multimodal: text + image)
   Parse JSON response → treatment, fertilizer, pesticide, prevention, chemicalClass
   Else: use on-device basic recommendations
        ↓
5. Build product research prompt
   Call Gemini (text only) → list of products with purchase URLs
   Fallback: on-device hardcoded suggestions
        ↓
6. Assemble full result map (plantName, diseaseName, cause, severity, confidence, treatment, fertilizer, pesticide, soilType, soilHealth, npk, prevention, chemicalClass, suitableCrops, weather, regionHint, productResearch, aiSource, etc.)
        ↓
7. Save to local JSON database (LocalDatabase)
   If user logged in → also save to Firestore
        ↓
8. Navigate to ResultsScreen (displays everything)
```

---

## Files Modified/Created

### Backend (Node.js) — simplified
- `backend/prisma/schema.prisma`: Added AI tracking fields (still used for optional cloud sync)
- `backend/src/controllers/scan.controller.ts`: Now accepts **client-provided analysis** and stores directly (no AI processing). If client analysis not provided, returns 501 (server AI disabled).
- The backend AI services (AIService, RecommendationService) remain but are no longer used by mobile. They can be removed in production if only mobile AI is desired.

### Mobile (Flutter) — major changes
- `mobile/lib/core/api/scanner_service.dart`: Complete rewrite — does all analysis on mobile, fetches weather, calls Gemini, stores locally/Firestore.
- `mobile/lib/core/ai/llm_service.dart`: Now supports multimodal (image + text) using Gemini Vision; reads API key from SharedPreferences.
- `mobile/lib/core/ai/on_device_ai_service.dart`: Unchanged — on-device TFLite provider.
- `mobile/lib/features/scanner/presentation/scanner_screen.dart`: Simplified UI, clean capture screen, removed model selector.
- `mobile/lib/features/scanner/presentation/results_screen.dart`: Cleaner cards, weather display, AI badge, product purchase buttons.
- `mobile/lib/features/dashboard/presentation/settings_screen.dart`: Added "Gemini API Key" input; saved to SharedPreferences.

---

## Configuration

### Gemini API Key (Optional)
1. Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Open the app → Settings → "Gemini API Key"
3. Paste the key and tap SAVE
4. Restart the app for cloud AI features to activate

### Backend URL (Optional)
- Only needed if you want to sync scans to your own server.
- Without it, scans are stored locally on device and optionally in Firestore if logged in.

---

## Features

✅ **Fully self-contained APK** — no external Python server needed  
✅ **On-device pest/disease detection** — works offline  
✅ **Real-time weather** — Open-Meteo direct, no API key  
✅ **Cloud AI enhancement** — Gemini Vision (if key provided)  
✅ **Product recommendations** with purchase links (Amazon/AgriBegri)  
✅ **Clean, modern UI** with weather card, confidence indicator, and detailed insights  
✅ **Local + Cloud storage** — JSON file locally, Firestore when logged in  

---

## Build & Run

```bash
cd mobile
flutter pub get
flutter run
```

**No additional setup** beyond inserting a Gemini key for advanced features.

---

## Notes

- The old YOLO Python microservice and its Node wrapper have been removed — they are no longer needed.
- The TFLite model remains bundled; it covers basic crop diseases and soil types (Indian context).
- Gemini responses are parsed as JSON; malformed responses are gracefully ignored and on-device data used instead.
- All network calls are made directly from the mobile app, reducing latency and infrastructure complexity.

Enjoy your 100% working, mobile-first NuKropAI!
