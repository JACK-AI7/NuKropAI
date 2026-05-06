from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Security, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
import io
import os
import time
import json
import cv2
import numpy as np
from PIL import Image
import gradio as gr

# --- Internal Modules ---
from .config import config
from .auth import get_api_key
from .model_manager import manager
from .redis_cache import redis_cache
from .websocket_manager import manager as ws_manager
from .prometheus_metrics import setup_metrics
from .ai_router import ai_router
from .forecast_engine import forecast_engine
from .ndvi_engine import ndvi_engine
from .qdrant_memory import qdrant_memory
from .celery_worker import process_mllm_task

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🌿 NuKropAI Enterprise Server Starting...")
    manager.load_all()
    await redis_cache.connect()
    yield
    await redis_cache.close()
    logger.info("👋 NuKropAI Server Stopped.")

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Instrumentation ---
setup_metrics(app)

# --- Gradio Admin UI ---
def create_admin_ui():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🌿 NuKropAI Enterprise Admin Panel")
        with gr.Tab("System Status"):
            uptime_val = gr.Number(label="Uptime (s)", value=0)
            status_btn = gr.Button("Refresh")
            status_btn.click(lambda: int(time.time() - manager.stats["start_time"]), outputs=uptime_val)
        with gr.Tab("Model Control"):
            gr.Markdown("OTA Updates and Model Reloading")
            reload_btn = gr.Button("Reload Models", variant="primary")
            reload_btn.click(manager.load_all)
    return demo

app.mount("/admin/ui", gr.mount_gradio_app(app, create_admin_ui(), path="/admin/ui"))

# --- Helper ---
def decode_image(file_bytes: bytes) -> Image.Image:
    try:
        img_array = np.frombuffer(file_bytes, np.uint8)
        bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Image decode failed: {e}")

# --- Core AI Routes ---
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": config.VERSION,
        "models_loaded": list(manager.models.keys()),
        "redis_active": redis_cache.client is not None
    }

@app.post("/analyze/crop", dependencies=[Depends(get_api_key)])
async def analyze_crop(file: UploadFile = File(...)):
    img_bytes = await file.read()
    
    # 1. Check Cache
    cached = await redis_cache.get_cached_result(img_bytes)
    if cached: return cached

    # 2. Inference
    img = decode_image(img_bytes)
    result = await ai_router.analyze_crop(img)
    
    # 3. Cache and Return
    await redis_cache.cache_result(img_bytes, result)
    return result

@app.get("/analytics/forecast", dependencies=[Depends(get_api_key)])
async def get_forecast(lat: float, lon: float):
    return forecast_engine.get_forecast(lat, lon)

@app.get("/analyze/satellite", dependencies=[Depends(get_api_key)])
async def analyze_satellite(lat: float, lon: float):
    return ndvi_engine.analyze_field(lat, lon)

@app.post("/memory/search", dependencies=[Depends(get_api_key)])
async def search_memory(query: str):
    return qdrant_memory.search(query)

# --- WebSocket for Real-time Detection ---
@app.websocket("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            img = decode_image(data)
            
            # Fast YOLO Inference for streaming
            pest_model = manager.get_model("pest")
            detections = []
            if pest_model:
                results = pest_model(img, verbose=False)
                for r in results:
                    for box in r.boxes:
                        detections.append({
                            "class": r.names[int(box.cls)],
                            "confidence": round(float(box.conf), 4),
                            "bbox": [round(v, 2) for v in box.xyxy[0].tolist()]
                        })
            await ws_manager.send_json({"detections": detections}, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WS Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, workers=1)
