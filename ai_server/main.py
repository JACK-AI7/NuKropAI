from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import uvicorn
import cv2
import numpy as np
import torch
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, pipeline
from typing import List, Optional
import os

app = FastAPI(title="NuKropAI Multi-Model Farming Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Model Registry (Lazy Loading) ---
models = {
    "pest": None,
    "maize": None,
    "plantnet": None,
    "agronomist": None
}

def get_pest_model():
    if models["pest"] is None:
        # Use hf-hub: prefix for correct Hugging Face model resolution
        try:
            models["pest"] = YOLO("hf-hub:underdogquality/yolo11s-pest-detection")
        except Exception as e:
            print(f"Error loading YOLO from HF: {e}")
            # Fallback to local download
            try:
                models["pest"] = YOLO("yolo11s.pt")
            except Exception as e2:
                print(f"Fallback YOLO load failed: {e2}")
                raise
    return models["pest"]

def get_maize_model():
    if models["maize"] is None:
        # Placeholder for transformers image classification
        models["maize"] = pipeline("image-classification", model="muAtarist/maize_disease_model")
    return models["maize"]

def get_agronomist():
    if models["agronomist"] is None:
        # Using a small LLM pipeline for advice
        models["agronomist"] = pipeline("text-generation", model="persadian/CropSeek-LLM", device_map="auto")
    return models["agronomist"]

@app.get("/")
async def root():
    return {"status": "NuKropAI Multi-Model Server is Running", "capabilities": list(models.keys())}

@app.post("/detect/pest")
async def detect_pest(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    model = get_pest_model()
    results = model(img)
    
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "box": box.xyxy[0].tolist(),
                "confidence": float(box.conf[0]),
                "name": r.names[int(box.cls[0])]
            })
    return {"detections": detections}

@app.post("/detect/maize")
async def detect_maize(file: UploadFile = File(...)):
    contents = await file.read()
    # Save temp file for pipeline
    with open("temp_maize.jpg", "wb") as f:
        f.write(contents)
    
    model = get_maize_model()
    results = model("temp_maize.jpg")
    os.remove("temp_maize.jpg")
    return {"results": results}

@app.post("/recommend/crop")
async def recommend_crop(n: float, p: float, k: float, temp: float, humidity: float, ph: float, rainfall: float):
    # Basic logic based on common NPK datasets (SF24/Crop-recommendation)
    # In a real app, this would load a saved .pkl or .joblib model
    # Returning a mock response for demonstration
    return {
        "recommended_crop": "Rice",
        "confidence": 0.95,
        "advice": f"With N:{n}, P:{p}, K:{k}, the soil is ideal for Rice."
    }

@app.post("/chat/agronomist")
async def chat_agronomist(prompt: str):
    # This might be slow on free tiers
    try:
        pipe = get_agronomist()
        response = pipe(prompt, max_length=150)
        return {"response": response[0]['generated_text']}
    except Exception as e:
        return {"response": f"AI Agronomist is busy. Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
