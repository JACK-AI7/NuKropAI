import cv2
import tempfile
import os
import asyncio
from fastapi import APIRouter, File, UploadFile, Depends
from pydantic import BaseModel
import httpx
import google.generativeai as genai

router = APIRouter()
HF_API = "https://api-inference.huggingface.co/models/nickmuchi/vit-finetuned-chestnut-disease"
HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY", "")

# 1. AI CROP DOCTOR (VIDEO TO SATELLITE ENGINE)
@router.post("/scan/video")
async def analyze_crop_video(file: UploadFile = File(...)):
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

    # Process all frames async via HF Model
    tasks = [process_image(f) for f in frames]
    results = await asyncio.gather(*tasks)

    disease_counts = {}
    severity_sum = 0
    for r in results:
        disease = r.get("label", "healthy")
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
        severity_sum += r.get("score", 0)

    main_disease = max(disease_counts, key=disease_counts.get) if disease_counts else "Unknown"

    return {
        "status": "success",
        "primary_issue": main_disease,
        "spread_confidence": (severity_sum / len(results) if results else 0) * 100,
        "frames_analyzed": len(frames),
        "treatment_plan": "Isolate region. Apply 5ml/L Neem Extract." # In Prod: DB fetch based on `main_disease`
    }

async def process_image(img_bytes: bytes):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        res = await client.post(HF_API, headers=headers, content=img_bytes)
        return res.json()[0] if res.status_code == 200 and res.json() else {}


# 2. RURAL AI ASSISTANT CONTEXT MEMORY
class ChatRequest(BaseModel):
    message: str
    farm_history: str
    language: str

@router.post("/chat/rural")
async def agronomy_chatbot(req: ChatRequest):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    You are NuKrop AI. A highly intelligent agrarian expert for a farmer.
    FARM CONTEXT HISTORY STORED LOCALLY:
    {req.farm_history}

    FARMER SAYS: {req.message}
    Answer in {req.language}. Keep it rural, concise, and professional. Output directly with NO formatting asterisks.
    """

    response = model.generate_content(prompt)
    return {"reply": response.text}