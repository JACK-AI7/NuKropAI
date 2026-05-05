"""
Microservice for agricultural pest detection using YOLO11.
Provides a REST API for real-time pest identification on the IP102 dataset.
Run with: uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
import time
import base64
import io
import json
import logging
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from PIL import Image
import cv2

# Try to import ultralytics; if not available, provide helpful error
try:
    from ultralytics import YOLO
except ImportError as e:
    raise ImportError(
        "ultralytics package is required. Install with: pip install ultralytics\n"
        "Also ensure torch is installed for your platform (CPU or CUDA)."
    ) from e

# Optional: huggingface_hub for auto-download
try:
    from huggingface_hub import hf_hub_download
    HAS_HF_HUB = True
except ImportError:
    HAS_HF_HUB = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AgriPest Detection Service",
    description="YOLO11-based pest detection for agricultural images (IP102 dataset)",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = os.getenv('YOLO_MODEL_PATH', 'yolo11s-pest-detection.pt')
CONF_THRESHOLD = float(os.getenv('YOLO_CONF_THRESHOLD', '0.25'))
IOU_THRESHOLD = float(os.getenv('YOLO_IOU_THRESHOLD', '0.45'))
PORT = int(os.getenv('YOLO_SERVICE_PORT', '8000'))
# HuggingFace config for auto-download
HF_REPO_ID = os.getenv('YOLO_HF_REPO', 'underdogquality/yolo11s-pest-detection')
HF_FILENAME = os.getenv('YOLO_HF_FILENAME', 'best.pt')

# Global model instance
model: Optional[YOLO] = None

class DetectionRequest(BaseModel):
    """Request with base64-encoded image."""
    image_base64: str
    filename: Optional[str] = None
    confidence: Optional[float] = None  # Override default confidence threshold

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class PestDetection(BaseModel):
    species: str
    confidence: float
    bbox: BoundingBox

class DetectionResponse(BaseModel):
    detections: List[PestDetection]
    count: int
    top_confidence: float
    processing_time: float
    model: str
    model_version: Optional[str] = None

def load_model() -> YOLO:
    """Load YOLO model on first use (lazy loading)."""
    global model
    if model is None:
        logger.info(f"Loading YOLO model from {MODEL_PATH}...")
        try:
            model_path = MODEL_PATH
            # If model file doesn't exist locally, attempt to download from HuggingFace
            if not os.path.exists(model_path):
                if not HAS_HF_HUB:
                    raise ImportError(
                        "Model file not found and huggingface_hub not installed. "
                        "Install with: pip install huggingface_hub, or manually download the model."
                    )
                logger.info(f"Model not found at {model_path}. Downloading from HuggingFace ({HF_REPO_ID})...")
                try:
                    model_path = hf_hub_download(repo_id=HF_REPO_ID, filename=HF_FILENAME)
                    logger.info(f"Model downloaded to {model_path}")
                except Exception as e:
                    raise FileNotFoundError(f"Failed to download model from HuggingFace: {e}")
            model = YOLO(model_path)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    return model

def decode_image(base64_str: str) -> np.ndarray:
    """Decode base64 string to OpenCV image (BGR)."""
    try:
        # Remove data URL prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',', 1)[1]
        img_data = base64.b64decode(base64_str)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image")
        return img
    except Exception as e:
        raise ValueError(f"Invalid base64 image: {e}")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        _ = load_model()
        return {
            "status": "healthy",
            "service": "agri-pest-detection",
            "model": "yolo11s-pest-detection",
            "model_loaded": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_loaded": False
        }

@app.post("/detect", response_model=DetectionResponse)
async def detect_pests(request: DetectionRequest):
    """
    Detect pests in an image.

    Provide a base64-encoded image. Returns a list of pest detections
    with species name, confidence, and bounding box coordinates.
    """
    start_time = time.time()
    logger.info("Received pest detection request")

    # Decode image
    try:
        img = decode_image(request.image_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image decode error: {e}")

    # Load model
    try:
        yolo = load_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

    # Run inference
    conf = request.confidence or CONF_THRESHOLD
    try:
        results = yolo(img, conf=conf, iou=IOU_THRESHOLD, verbose=False)
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    # Parse results
    detections: List[Dict[str, Any]] = []
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy()  # x1, y1, x2, y2
                conf_val = float(box.conf[0])
                cls_id = int(box.cls[0])
                class_name = yolo.names[cls_id]

                detections.append({
                    "species": class_name,
                    "confidence": conf_val,
                    "bbox": {
                        "x1": float(xyxy[0]),
                        "y1": float(xyxy[1]),
                        "x2": float(xyxy[2]),
                        "y2": float(xyxy[3])
                    }
                })

    # Sort by confidence descending
    detections.sort(key=lambda d: d["confidence"], reverse=True)

    processing_time = time.time() - start_time
    top_conf = detections[0]["confidence"] if detections else 0.0

    logger.info(f"Detected {len(detections)} pests in {processing_time:.2f}s")

    return DetectionResponse(
        detections=[PestDetection(**d) for d in detections],
        count=len(detections),
        top_confidence=top_conf,
        processing_time=processing_time,
        model="yolo11s-pest-detection",
        model_version=os.getenv('YOLO_MODEL_VERSION', 'v1.0')
    )

# Optional: multipart endpoint
@app.post("/detect/multipart", response_model=DetectionResponse)
async def detect_pests_multipart(image: UploadFile = File(...)):
    """Alternative endpoint accepting multipart/form-data."""
    contents = await image.read()
    base64_str = base64.b64encode(contents).decode('utf-8')
    return await detect_pests(DetectionRequest(image_base64=base64_str, filename=image.filename))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting ML service on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
