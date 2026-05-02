# NuKropAi Pro — Deployment Guide

## Overview
**100% Free AI** — No paid APIs. Works fully offline. Two deployment modes available.

---

## Mode 1: Desktop Backend + Mobile (Recommended)
Uses **Ollama** for powerful on-device AI on your computer. Backend handles scans; mobile app connects via WiFi/emulator.

### Prerequisites
- Node.js (v18+)
- **Ollama** installed from https://ollama.ai

### Setup
1. Clone repo & `cd kropAI`
2. **Backend**:
   ```bash
   cd backend
   npm install
   npx prisma migrate dev --name init
   npm run dev
   ```
3. **Install AI models**:
   - Windows: `setup_ollama.bat`
   - Mac/Linux: `./setup_ollama.sh`
4. **Mobile**:
   - **Emulator**: No config needed (uses `10.0.2.2:3000`)
   - **Real device**: Edit `mobile/lib/core/config/constants.dart` → set `baseUrl` to your computer's LAN IP (e.g., `http://192.168.1.5:3000/api`)
5. Install `Nunukropai.apk` on Android

**Connectivity**: Mobile and computer must be on the same WiFi network (or use emulator).

---

## Mode 2: 100% Offline Mobile (Zero Server)
The app runs **entirely on-device** with TensorFlow Lite. No computer, no network, no backend.

### Setup
1. **Download ML model**:
   - Windows: Run `download_model.bat`
   - Mac/Linux: Run `./download_model.sh`
   
   This downloads the TFLite crop disease classifier (~20MB) into `mobile/assets/models/`

2. **Install APK**:
   ```bash
   cd mobile
   flutter install
   ```
   Or transfer `Nunukropai.apk` to device.

3. **Done** — the app will automatically load the on-device AI model on first scan.

**Note**: Offline mode uses a smaller model. For highest accuracy, use Mode 1 with Ollama.

---

## Backend Commands
| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server (hot reload) |
| `npm run build` | Compile to JavaScript |
| `npm start` | Run production build |
| `npx prisma studio` | View/edit database |

---

## Troubleshooting

### Mobile can't reach backend?
- Ensure both devices are on same network
- Check firewall: allow Node.js through (port 3000)
- For emulator: `10.0.2.2:3000` always works

### Ollama not responding?
- Verify service is running: `ollama serve` (runs in background)
- Test models: `ollama list` should show `llava:13b` and `phi3:mini`
- Restart backend after pulling models

### App stuck on loading?
- First run downloads model (~20s). Wait.
- Check logs: `flutter run -v`
- Delete app data & reinstall

---

## Git Repository
- **Main Branch**: `main`
- All commits are production-ready.

---
*KropAi: Farming intelligence for everyone, powered by free open-source AI.*
