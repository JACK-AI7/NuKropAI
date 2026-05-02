# 🌿 KropAi — Advanced AI Farming Assistant

**KropAi** is a production-level, fullstack agricultural platform designed to empower farmers with real-time AI diagnostics, weather-aware intelligence, and professional expert advice. Built with a focus on accessibility and performance, KropAi brings a world-class diagnostic laboratory directly to the farmer's pocket.

**FREE AI — No API Costs**: KropAi uses **Ollama** to run powerful open-source AI models locally on your machine. No per-call fees, no rate limits, complete privacy.

---

## 🌟 What KropAi Can Do

### 🔍 1. Precision AI Diagnostics
- **Leaf Scan**: Instantly detect crop diseases with >90% AI confidence using your camera or gallery.
- **Soil Analysis**: Analyze soil health and receive personalized nutrient recommendations.
- **Real-Time Processing**: High-speed image compression ensures diagnostic results in seconds, even on 3G networks.

### 🧠 2. Smart Weather-Aware Recommendations
- **Contextual Intelligence**: The app fetches live weather data (Temp & Humidity) to refine its advice.
- **Fungal Warnings**: Automatically alerts farmers of high fungal risks during humid conditions.
- **Heat Stress Alerts**: Provides irrigation adjustments based on real-time temperature spikes.

### 📊 3. Professional NPK Visualizations
- **Nutrient Dashboard**: View Nitrogen, Phosphorus, and Potassium levels in professional-grade bar charts.
- **Dosage Recipes**: Receive exact fertilizer (Urea, DAP, NPK) and pesticide dosages tailored to your specific crop and region.

### 🗣️ 4. Multi-Language & Voice Accessibility
- **Three Core Languages**: Full support for **English**, **Hindi (🇮🇳)**, and **Telugu (🇮🇳)**.
- **Voice Advice (TTS)**: The app **speaks** the diagnosis and treatment plan aloud in the selected language, ensuring accessibility for all farmers.

### 🛡️ 5. Resilient "Always-Working" Architecture
- **Offline Fallback**: Built-in standalone data ensures the app provides expert advice even when internet connectivity is lost.
- **Local Persistence**: Scan history is stored locally (SQLite) and synced with the cloud (PostgreSQL/Prisma).

---

## 🎨 Premium minimalist "Cloud" UI
Inspired by modern, high-end minimalist design, KropAi features:
- **Neo-Glassmorphic Aesthetic**: Light gray backgrounds with pure white cards.
- **High-End Typography**: Bold, clear diagnostic headers for maximum readability.
- **Micro-Interactions**: Sunrise/Sunset widgets and soft animations (AnimateDo).

---

## 🛠️ Technical Stack
- **Frontend**: Flutter (Riverpod for state management)
- **Backend**: Node.js, Express, TypeScript
- **Database**: SQLite (Local), Prisma (ORM)
- **AI**: **Ollama + Llava (Vision) + Phi-3 (Chat)** — 100% free, runs locally, no API keys needed
- **Optimizations**: `flutter_image_compress` for fast uploads, `fl_chart` for NPK visuals.

---

## 🚀 Getting Started

### Quick Start (5 Minutes)

#### Option A: Desktop with Backend + Mobile (Best AI Quality)
Uses powerful Ollama models running on your computer.

1. **Install Ollama** (Free AI) from https://ollama.ai
2. Run `setup_ollama.bat` (Windows) or `./setup_ollama.sh` (Mac/Linux)
   - This pulls `llava:13b` (vision) and `phi3:mini` (chat)
3. **Backend**: `cd backend && npm install && npm run dev`
4. **Mobile**:
   - If using Android emulator: API URL is pre-set to `http://10.0.2.2:3000/api`
   - If using real device: edit `mobile/lib/core/config/constants.dart` with your computer's IP
   - Install `Nunukropai.apk` and scan!

#### Option B: 100% Offline Mobile (No Server)
App runs entirely on-device with TensorFlow Lite. **No internet required**.

1. Download the ML model:
   - Windows: Run `download_model.bat`
   - Mac/Linux: Run `./download_model.sh`
2. Install the APK: `Nunukropai.apk`
3. All processing happens on your phone — completely offline

---

## 💡 AI Options Comparison

| Mode | Backend Required | Model Size | AI Quality | Internet |
|------|-----------------|------------|------------|----------|
| **Ollama Backend** | Yes (laptop) | ~8GB total | Excellent (Llava 13B) | Optional (for weather) |
| **On-Device TFLite** | No | ~20MB app bundle | Good (MobileNet) | **Not required** |
| **Rule-Based Fallback** | No | 0KB | Basic | Not required |

**Recommendation**: Use Option A for best results, Option B for offline-only scenarios.

---

## 📱 Mobile App
Pre-built APK: `Nunukropai.apk` (63 MB)

Transfer to Android device, enable "Install from Unknown Sources", and install.

---

*Built with ❤️ for the global farming community. Powered by free, open-source AI.*
