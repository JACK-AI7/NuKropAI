import cv2
import tempfile
import os
import asyncio
from fastapi import APIRouter, File, UploadFile, Depends, UploadFile as UploadFileType
from pydantic import BaseModel
from ..core.firebase_auth import verify_firebase_token
from ...model_manager import ai_core

router = APIRouter()

# 1. AI CROP DOCTOR (IMAGE ANALYSIS)
@router.post("/scan/image")
async def analyze_crop_image(file: UploadFile = File(...), token: dict = Depends(verify_firebase_token)):
    """Analyze single crop image for diseases using dynamic AI loading"""
    img_bytes = await file.read()

    # Convert bytes to PIL Image
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    # Use AI Manager for dynamic loading
    diagnosis = ai_core.scan_leaf_disease(img)

    # Clean up memory after use
    ai_core.kill_mode('vision')

    return {
        "status": "success",
        "diagnosis": diagnosis,
        "treatment_plan": "Isolate region. Apply 5ml/L Neem Extract."
    }

# 2. AI CROP DOCTOR (VIDEO TO SATELLITE ENGINE)
@router.post("/scan/video")
async def analyze_crop_video(file: UploadFile = File(...), token: dict = Depends(verify_firebase_token)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

        cap = cv2.VideoCapture(tmp.name)
        frames, frame_count = [], 0

        while cap.isOpened() and len(frames) < 6:
            ret, frame = cap.read()
            if not ret: break
            if frame_count % 15 == 0:  # Sample 2 fps
                success, buffer = cv2.imencode('.jpg', frame)
                if success: frames.append(buffer.tobytes())
            frame_count += 1
        cap.release()
    finally:
        os.remove(tmp.name)

    # Process all frames async via AI Manager
    tasks = [process_image_with_ai(f) for f in frames]
    results = await asyncio.gather(*tasks)

    disease_counts = {}
    severity_sum = 0
    for r in results:
        disease = r.get("disease", "healthy")
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
        severity_sum += r.get("confidence", 0)

    main_disease = max(disease_counts, key=disease_counts.get) if disease_counts else "Unknown"

    return {
        "status": "success",
        "primary_issue": main_disease,
        "spread_confidence": (severity_sum / len(results) if results else 0),
        "frames_analyzed": len(frames),
        "treatment_plan": "Isolate region. Apply 5ml/L Neem Extract."
    }

async def process_image_with_ai(img_bytes: bytes):
    """Process single frame using AI Manager"""
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    diagnosis = ai_core.scan_leaf_disease(img)
    return diagnosis

# 3. VOICE TRANSCRIPTION (MULTILINGUAL)
@router.post("/voice/transcribe")
async def transcribe_audio(file: UploadFile = File(...), token: dict = Depends(verify_firebase_token)):
    """Convert audio to text using Whisper (supports Hindi/Telugu/English)"""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    try:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

        # Use AI Manager for voice transcription
        text = ai_core.translate_audio_to_text(tmp.name)

        # Clean up memory
        ai_core.kill_mode('whisper')

        return {
            "status": "success",
            "transcription": text,
            "language": "detected"  # Whisper auto-detects
        }
    finally:
        os.remove(tmp.name)

# 4. RURAL AI ASSISTANT CONTEXT MEMORY
class ChatRequest(BaseModel):
    message: str
    farm_history: str
    language: str = "en"

@router.post("/chat/rural")
async def agronomy_chatbot(req: ChatRequest, token: dict = Depends(verify_firebase_token)):
    """Offline LLM Agronomy assistant with farm context"""
    # Use AI Manager for offline chat
    response = ai_core.agronomy_chat(req.message, req.farm_history)

    # Clean up memory
    ai_core.kill_mode('llm')

    return {"reply": response}