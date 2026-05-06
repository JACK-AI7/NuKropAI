from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api import ai_crops_router
from .core.firebase_auth import verify_firebase_token
from ...model_manager import ai_core
import firebase_admin
from firebase_admin import credentials, auth
import os
import json

app = FastAPI(title="NuKropAI Core Agri-OS Backend", version="2.0-PROD")

# ERROR PREVENTION: Allow all connections securely to prevent Flutter CORS Blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your flutter domain later if building Web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def initialize_firebase():
    # 1. We wrap initialization in a strict Try-Catch.
    try:
        # Load string from Environment variable instead of physical file for high security.
        raw_cred = os.environ.get("FIREBASE_ADMIN_CREDENTIALS")
        if not raw_cred:
            print("🚨 ERROR: FIREBASE_ADMIN_CREDENTIALS missing!")
            return

        cred_dict = json.loads(raw_cred)
        cred = credentials.Certificate(cred_dict)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            print("✅ NuKrop AI Cloud Authenticated securely.")

        # Initialize AI stats
        ai_core.stats = {"start_time": __import__("time").time()}

    except Exception as e:
        print(f"🔥 FATAL ERROR: Failed to boot backend security! {e}")
        # Optionally exit app to prevent fake requests from entering processing

app.include_router(ai_crops_router.router, prefix="/api/v1", dependencies=[Depends(verify_firebase_token)])

@app.get("/health")
def health():
    return {
        "status": "Online",
        "mode": "Advanced Multi-Modal AI Active",
        "firebase": bool(firebase_admin._apps),
        "gpu_available": ai_core.device.startswith("cuda"),
        "active_models": list(ai_core.active_models.keys())
    }