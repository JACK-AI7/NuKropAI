from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import uvicorn
import shutil
import os
import cv2
import numpy as np
from typing import List

app = FastAPI(title="NuKropAI YOLOv8 Server")

# Enable CORS for mobile app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv8 model (downloads automatically on first run if not present)
# Using yolov8n.pt for speed on free tier servers
MODEL_PATH = "yolov8n.pt"
model = YOLO(MODEL_PATH)

@app.get("/")
async def root():
    return {"status": "NuKropAI Server is Running", "model": MODEL_PATH}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    # Run inference
    results = model(img)
    
    detections = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Get box coordinates, confidence, and class
            b = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = r.names[cls]
            
            detections.append({
                "box": b,
                "confidence": conf,
                "class": cls,
                "name": name
            })

    return {
        "count": len(detections),
        "detections": detections
    }

if __name__ == "__main__":
    # Port 7860 is standard for Hugging Face Spaces
    uvicorn.run(app, host="0.0.0.0", port=7860)
