---
title: NuKropAI Farming AI
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
# NuKropAI — Enterprise Agricultural AI Backend

Multimodal AI platform for crop disease diagnosis, pest detection, soil analysis, and smart farming guidance.

## Features
- 🌿 Crop disease & pest detection (Qwen2.5-VL)
- 🧪 Soil & nutrient analysis
- 💊 Fertilizer & irrigation recommendations
- 🤖 Multilingual agricultural chatbot
- ⚡ GPU-optimized 4-bit quantized inference
- 📡 WebSocket streaming responses
- 🗂️ Vector memory via Qdrant

## API Endpoints
- `GET /` — Status
- `GET /health` — Health check
- `POST /diagnose` — Image + question → full diagnosis
- `POST /chat` — Text-only agricultural assistant
- `WS /ws/{client_id}` — WebSocket streaming
