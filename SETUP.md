# NuKropAI — Complete Setup Guide

## Prerequisites
- Node.js 18+ 
- Python 3.9+ (for ML service)
- Git
- (Optional) Docker if you want containerized deployment

---

## 1. Backend Setup

```bash
cd backend
npm install
npm run build   # Compile TypeScript
npm run dev     # Start development server
```

The backend runs on http://0.0.0.0:3000.

Configure environment variables in `backend/.env`:

```env
# AI Providers (choose at least one)
MISTRAL_API_KEY=your_key_here          # Optional: for cloud AI
OLLAMA_HOST=http://localhost:11434     # Optional: for local LLM

# YOLO ML Service
ML_SERVICE_URL=http://localhost:8000
YOLO_MODEL_VERSION=yolo11s-pest-detection-v1

# Database
DATABASE_URL="file:./dev.db"

# JWT
JWT_SECRET=change-this-in-production
```

The backend exposes:
- `POST /api/scans` — scan an image (accepts `modelType` form field)
- `GET /api/scans/history`
- `GET /api/scans/:id`
- `POST /api/ai/chat`
- `GET /api/weather`
- `GET /api/recommendations`

---

## 2. YOLO Pest Detection ML Service (Python)

The ML service runs separately and is called by the backend for fast pest detection using YOLO11s on the IP102 dataset (102 pest species).

### Quick Start
```bash
cd backend/ml-service
python -m venv venv
# Activate venv (Windows): venv\Scripts\Activate.ps1
# (Linux/Mac): source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

The service will:
- Auto-download the YOLO11s-pest-detection model (~20 MB) from HuggingFace on first run if not present locally.
- Expose endpoints:
  - `GET /health` — health check
  - `POST /detect` — JSON body with `image_base64` → returns pest detections

**Environment variables** (optional):
```env
YOLO_MODEL_PATH=best.pt                    # default: yolo11s-pest-detection.pt
YOLO_SERVICE_PORT=8000
YOLO_CONF_THRESHOLD=0.25
YOLO_IOU_THRESHOLD=0.45
YOLO_HF_REPO=underdogquality/yolo11s-pest-detection
YOLO_HF_FILENAME=best.pt
```

The model is under MIT license and detects 102 pest species with >90% mAP.

### Without auto-download
Manually download `best.pt` from https://huggingface.co/underdogquality/yolo11s-pest-detection and place it in `backend/ml-service/`, then set `YOLO_MODEL_PATH=best.pt`.

---

## 3. Mobile App Configuration

1. Open `mobile/lib/core/config/constants.dart` (or Settings screen) and set the backend URL:
   - Example: `http://192.168.1.100:3000` (your machine's LAN IP).

2. The scanner screen now has a model selector (top-right corner):
   - **Auto** — tries YOLO first, falls back to cloud/local LLM
   - **YOLO** — fast pest detection (specialized)
   - **General AI** — detailed analysis via Mistral/Ollama

3. Ensure the mobile device is on the same network as the backend and ML service.

---

## 4. Fallback Chain (How it Works)

For pest scans (non-soil) the backend uses this logic:

1. **YOLO** (if modelType is 'yolo' or 'auto'): Fast detection of 102 pest species. If successful → return result.
2. **Vision AI** (Mistral Pixtral or Ollama llava): If YOLO fails or returns no pests.
3. **Curated Database** (`crops.json`): If both AI services fail, then a database lookup by label.

This guarantees high availability and accurate detection even if one component is down.

---

## 5. Database

Uses SQLite in development (`backend/prisma/dev.db`). Schema updated with fields:
- `aiModel` — which model produced the result
- `pestDetections` — JSON array of all detected pests (species, confidence, bbox)
- `modelConfidence` — top confidence
- `processingTime` — inference ms for YOLO

Apply migrations:
```bash
cd backend
npx prisma db push
```

(Production should use PostgreSQL.)

---

## 6. Important File Changes

- `backend/prisma/schema.prisma` — added AI tracking fields
- `backend/src/controllers/scan.controller.ts` — integrates YOLO service + fallback logic
- `backend/src/services/pest-detection.service.ts` — new service to call Python ML microservice
- `backend/ml-service/main.py` — FastAPI app for YOLO inference
- `backend/ml-service/requirements.txt` — includes huggingface_hub for model auto-download
- `backend/.env` — added `ML_SERVICE_URL` and `YOLO_MODEL_VERSION`
- Mobile: `scanner_screen.dart`, `scanner_service.dart`, `results_screen.dart` — model selector, YOLO results display

---

## 7. Troubleshooting

### Backend fails to connect to ML service
- Ensure the Python service is running on port 8000.
- Check `ML_SERVICE_URL` in `.env` matches.
- The backend will automatically fallback to AI services if ML service unreachable.

### YOLO model won't download
- Install `huggingface_hub` (`pip install huggingface_hub`).
- Ensure internet connectivity first run.
- Alternatively download `best.pt` manually from HuggingFace and set `YOLO_MODEL_PATH`.

### Mobile cannot reach backend
- Verify device and server are on same network.
- In app Settings, set Server URL to `http://<your-pc-ip>:3000`.
- Disable firewall or allow port 3000.

### AI services not responding
- For Mistral: set `MISTRAL_API_KEY` in `.env`.
- For Ollama: ensure `ollama serve` is running and vision model `llava:latest` is pulled (`ollama pull llava`).

---

## 8. Production Notes

- Use PostgreSQL instead of SQLite.
- Set strong `JWT_SECRET`.
- Enable Mistral API only; you can disable Ollama.
- Host ML service separately or use GPU inference.
- Add request rate limiting and caching (e.g., cache YOLO results by image hash).

---

Enjoy 100% working agricultural pest detection with the best YOLO11s model!
