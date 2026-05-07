"""
NuKropAI — Enterprise Agricultural AI Backend
FastAPI application with multimodal image diagnosis, text chat,
WebSocket streaming, and health monitoring.
"""

import os
import uuid
import logging
import asyncio
import time
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ai_router import ai_router
from inference_router import inference_router
from model_manager import model_manager
from services.diagnosis_service import diagnosis_service
from services.soil_service import soil_service
from services.pest_service import pest_service
from services.fertilizer_service import fertilizer_service
from services.irrigation_service import irrigation_service
from utils.gpu_utils import log_gpu_status, get_device, get_vram_gb

# ------------------------------------------------------------------ #
#  Logging                                                             #
# ------------------------------------------------------------------ #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("nukropai.main")

# ------------------------------------------------------------------ #
#  Startup / Shutdown                                                  #
# ------------------------------------------------------------------ #

TEMP_DIR = Path("temp")
CACHE_DIR = Path("cache")
WEIGHTS_DIR = Path("weights")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create required directories and log startup info."""
    TEMP_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    WEIGHTS_DIR.mkdir(exist_ok=True)

    logger.info("=" * 60)
    logger.info("NuKropAI Agricultural AI Backend — Starting")
    logger.info(f"Device: {get_device()} | VRAM: {get_vram_gb():.1f} GB")
    logger.info("=" * 60)

    yield  # Application is running

    logger.info("NuKropAI shutting down — unloading models…")
    model_manager.unload_model()

# ------------------------------------------------------------------ #
#  App                                                                 #
# ------------------------------------------------------------------ #

app = FastAPI(
    title="NuKropAI Agricultural AI",
    description="Enterprise multimodal AI platform for precision agriculture",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------ #
#  WebSocket Manager                                                   #
# ------------------------------------------------------------------ #

active_connections: dict[str, WebSocket] = {}


async def broadcast(client_id: str, message: dict):
    ws = active_connections.get(client_id)
    if ws:
        try:
            await ws.send_json(message)
        except Exception:
            active_connections.pop(client_id, None)

# ------------------------------------------------------------------ #
#  Pydantic models                                                     #
# ------------------------------------------------------------------ #

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    history: list[dict] = []


class ChatResponse(BaseModel):
    success: bool
    reply: str
    model_used: str
    latency_ms: int

# ------------------------------------------------------------------ #
#  Routes                                                              #
# ------------------------------------------------------------------ #

@app.get("/", tags=["Status"])
async def root():
    return {
        "service": "NuKropAI Agricultural AI",
        "version": "1.0.0",
        "status": "running",
        "device": get_device(),
        "vram_gb": round(get_vram_gb(), 2),
    }


@app.get("/health", tags=["Status"])
async def health():
    log_gpu_status()
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "device": get_device(),
        "vram_gb": round(get_vram_gb(), 2),
        "model_loaded": model_manager.current_name,
    }


@app.post("/diagnose", tags=["AI"])
async def diagnose(
    image: UploadFile = File(...),
    question: str = Form("Analyze this crop image"),
    language: str = Form("en"),
):
    """
    Upload a crop/plant image and ask a question.
    Returns full agricultural diagnosis: disease, soil, pest, fertilizer, irrigation.
    """
    # Save uploaded image to temp directory
    file_path = TEMP_DIR / f"{uuid.uuid4()}.jpg"

    try:
        contents = await image.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty image file.")

        file_path.write_bytes(contents)

        t0 = time.time()

        # Route to best model
        model_name = ai_router.choose_model(question)
        system_prompt = ai_router.build_system_prompt(question)
        prompt = diagnosis_service.build_prompt(question)

        # Run multimodal inference
        response = inference_router.run(
            model_name=model_name,
            image_path=str(file_path),
            prompt=prompt,
            system_prompt=system_prompt,
            max_new_tokens=512,
        )

        # Enrich with domain-specific analysis
        soil = soil_service.analyze(response)
        pest = pest_service.analyze(response)
        fertilizer = fertilizer_service.recommend("auto")
        irrigation = irrigation_service.advise()

        latency_ms = int((time.time() - t0) * 1000)
        logger.info(f"Diagnosis complete in {latency_ms}ms using '{model_name}'")

        return {
            "success": True,
            "model_used": model_name,
            "diagnosis": response,
            "soil_analysis": soil,
            "pest_analysis": pest,
            "fertilizer": fertilizer,
            "irrigation": irrigation,
            "latency_ms": latency_ms,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Diagnose endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass


@app.post("/chat", response_model=ChatResponse, tags=["AI"])
async def chat(req: ChatRequest):
    """
    Text-only agricultural chatbot — no image required.
    Uses the default model to answer farming questions.
    """
    from config import DEFAULT_MODEL

    t0 = time.time()
    try:
        model_name = ai_router.choose_model(req.message)
        system_prompt = ai_router.build_system_prompt(req.message)

        # For text-only chat, we pass a placeholder 1×1 white image
        # so the VL model still functions correctly
        placeholder_path = TEMP_DIR / f"chat_{uuid.uuid4()}.jpg"

        try:
            from PIL import Image as PILImage
            img = PILImage.new("RGB", (64, 64), color=(255, 255, 255))
            img.save(str(placeholder_path))

            reply = inference_router.run(
                model_name=model_name,
                image_path=str(placeholder_path),
                prompt=req.message,
                system_prompt=system_prompt,
                max_new_tokens=384,
            )
        finally:
            try:
                placeholder_path.unlink(missing_ok=True)
            except Exception:
                pass

        latency_ms = int((time.time() - t0) * 1000)

        return ChatResponse(
            success=True,
            reply=reply,
            model_used=model_name,
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket for real-time streaming agricultural chat.
    Client sends: {"message": "...", "language": "en"}
    Server responds with streaming tokens.
    """
    await websocket.accept()
    active_connections[client_id] = websocket
    logger.info(f"WebSocket connected: {client_id}")

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            if not message:
                await websocket.send_json({"error": "Empty message"})
                continue

            await websocket.send_json({"status": "processing", "message": "Analyzing…"})

            try:
                model_name = ai_router.choose_model(message)
                system_prompt = ai_router.build_system_prompt(message)

                # Generate response (non-streaming fallback for VL model)
                placeholder_path = TEMP_DIR / f"ws_{uuid.uuid4()}.jpg"
                try:
                    from PIL import Image as PILImage
                    PILImage.new("RGB", (64, 64), (255, 255, 255)).save(str(placeholder_path))

                    reply = inference_router.run(
                        model_name=model_name,
                        image_path=str(placeholder_path),
                        prompt=message,
                        system_prompt=system_prompt,
                        max_new_tokens=256,
                    )
                finally:
                    try:
                        placeholder_path.unlink(missing_ok=True)
                    except Exception:
                        pass

                await websocket.send_json({
                    "status": "done",
                    "reply": reply,
                    "model_used": model_name,
                })

            except Exception as e:
                logger.error(f"WebSocket inference error: {e}")
                await websocket.send_json({
                    "status": "error",
                    "error": str(e),
                })

    except WebSocketDisconnect:
        active_connections.pop(client_id, None)
        logger.info(f"WebSocket disconnected: {client_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        active_connections.pop(client_id, None)
