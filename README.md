---
title: NukropAI Farming AI
emoji: 🌿
colorFrom: green
colorTo: green
sdk: docker
pinned: false
---

# 🌿 NuKropAI Ultimate

**AI-Powered Crop Disease Detection & Agricultural Intelligence Platform for Indian Farmers**

[![Flutter](https://img.shields.io/badge/Flutter-3.41.8-02569B?logo=flutter)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.11.5-0175C2?logo=dart)](https://dart.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)](https://www.typescriptlang.org)
[![Firebase](https://img.shields.io/badge/Firebase-Connected-FFCA28?logo=firebase)](https://firebase.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🚀 Overview

NuKropAI is a production-grade agricultural AI platform that provides:

- 📷 **Crop disease detection** — on-device TFLite + Hugging Face cloud AI fallback
- 🌱 **Soil analysis** — type, health, NPK recommendations
- 🌤️ **Real-time weather** — Open-Meteo integration (no API key required)
- 🤖 **AI agronomist chat** — Gemini + Mistral + Ollama multi-model support
- 📍 **GPS-based regional advice** — India-specific crop/pest/fertilizer recommendations
- 🛒 **Product research** — AI-generated purchase suggestions with Amazon.in links
- 🔊 **Voice TTS** — multilingual text-to-speech for rural accessibility
- 🗺️ **Satellite analysis** — NDVI & forecast via backend API
- 📊 **Scan history** — Firestore-synced with local SQLite fallback

---

## 📁 Repository Structure

```
NuKropAI/
├── mobile/              # Flutter Android application
│   ├── lib/             # Dart source code
│   ├── android/         # Android native configs
│   └── assets/          # Models, images, fonts
├── backend/             # Node.js/TypeScript/Express API
│   ├── src/             # TypeScript source
│   ├── prisma/          # Database schema
│   └── dist/            # Compiled JS output
├── ai_server/           # Python/FastAPI AI inference (Hugging Face Spaces)
├── firebase/            # Firebase security rules & indexes
├── releases/
│   ├── apk/             # Release APK builds
│   └── aab/             # Release AAB builds
├── .github/             # CI/CD workflows
├── README.md
└── DEPLOYMENT_GUIDE.md
```

---

## 📦 Latest Release Artifacts

| Artifact | Size | Path |
|----------|------|------|
| Universal APK | ~86.5 MB | `releases/apk/NuKropAI-release.apk` |
| AAB (Play Store) | ~60.6 MB | `releases/aab/NuKropAI-release.aab` |
| ARM64 APK | Smaller | `releases/apk/split/app-arm64-v8a-release.apk` |
| ARM APK | Smaller | `releases/apk/split/app-armeabi-v7a-release.apk` |
| x86_64 APK | Smaller | `releases/apk/split/app-x86_64-release.apk` |

> **Note:** APKs are unsigned for direct sideloading. For Play Store, use the signed AAB via your keystore.

---

## 🛠️ Tech Stack

### Mobile (Flutter)
| Package | Purpose |
|---------|---------|
| `flutter_riverpod 2.6` | State management |
| `firebase_core/auth/firestore/storage` | Firebase integration |
| `firebase_remote_config` | Dynamic configuration |
| `google_generative_ai` | Gemini AI |
| `tflite_flutter` | On-device ML inference |
| `camera + image_picker` | Image capture |
| `geolocator + geocoding` | GPS & location |
| `flutter_tts` | Text-to-speech |
| `flutter_map` | Maps |
| `dio` | HTTP client |
| `sqflite` | Local database |
| `google_sign_in` | Google OAuth |

### Backend (Node.js/TypeScript)
| Package | Purpose |
|---------|---------|
| `express` | HTTP server |
| `@prisma/client` | ORM |
| `firebase-admin` | Server-side Firebase |
| `ioredis` | Redis caching |
| `multer` | File uploads |
| `helmet + cors` | Security |
| Mistral API | Vision & chat AI |
| Ollama | Local LLM fallback |

### AI Server (Python/FastAPI)
- Hugging Face Spaces deployment
- YOLO11 pest detection
- Plant disease classification
- WebSocket real-time inference

---

## ⚙️ Setup & Development

### Prerequisites
- Flutter 3.41.8+ (`flutter --version`)
- Dart 3.11.5+
- Node.js 18+
- Android SDK (API 34+)

### Flutter Mobile

```bash
cd mobile
flutter pub get
flutter run                          # Debug mode
flutter build apk --release          # Release APK
flutter build appbundle --release    # Play Store AAB
```

### Backend

```bash
cd backend
npm install
cp .env.example .env                 # Configure secrets
npx prisma generate
npx prisma migrate dev
npm run dev                          # Development
npm run build                        # Production build
npm start                            # Run compiled
```

### Environment Variables (Backend)

```env
# Required
DATABASE_URL=postgresql://...
FIREBASE_PROJECT_ID=sigma-gateway-477509-a4

# Optional AI providers (at least one recommended)
MISTRAL_API_KEY=your_key_here
OLLAMA_HOST=http://localhost:11434
OLLAMA_VISION_MODEL=llava:latest
OLLAMA_CHAT_MODEL=phi3:mini

# Optional services
REDIS_URL=redis://...
QDRANT_URL=http://localhost:6333
JWT_SECRET=your_jwt_secret

# Server
PORT=3000
NODE_ENV=production
ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 🔥 Firebase Configuration

Firebase project: **`sigma-gateway-477509-a4`**

Services enabled:
- ✅ Authentication (Email/Password + Google Sign-In)
- ✅ Cloud Firestore (scan history, user data)
- ✅ Firebase Storage (image uploads)
- ✅ Remote Config (API URLs, feature flags)
- ✅ Analytics

The `google-services.json` is pre-configured for the project. No changes needed unless switching Firebase projects.

---

## 🤖 AI Architecture

```
Mobile App
    │
    ├── On-device TFLite (offline-first)
    │       └── crop_disease_model.tflite
    │
    ├── Cloud AI (Hugging Face)
    │       ├── Disease classification
    │       ├── Pest detection (YOLO11)
    │       └── Soil classification
    │
    ├── Gemini (google_generative_ai)
    │       └── Multimodal analysis + chat
    │
    └── Backend API
            ├── Mistral Vision (primary)
            └── Ollama (local fallback)
```

**Fallback chain:** On-device → Hugging Face → Gemini → Backend Mistral → Backend Ollama

---

## 🚀 Deployment

### Android
1. Add keystore to `mobile/android/` and configure `key.properties`
2. `flutter build appbundle --release`
3. Upload `releases/aab/NuKropAI-release.aab` to Play Console

### Backend (Railway / Render)
1. Connect GitHub repo → auto-deploy `backend/` directory
2. Set environment variables in dashboard
3. `npm run build && npm start`

### AI Server (Hugging Face Spaces)
1. Push `ai_server/` directory contents to a HF Space
2. Update `RemoteConfigService.aiServerUrl` in Firebase Remote Config

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full details.

---

## 📊 Build Status

| Component | Status |
|-----------|--------|
| Flutter analyze | ✅ 0 errors |
| TypeScript (tsc) | ✅ 0 errors |
| Release APK | ✅ Built |
| Release AAB | ✅ Built |
| Backend build | ✅ Compiled |

---

## 🌾 Target Users

Indian smallholder farmers needing:
- Affordable, offline-capable crop disease identification
- Regional language support (TTS)
- GPS-tagged field records
- Locally relevant pesticide/fertilizer recommendations

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Built with ❤️ for Indian agriculture*
