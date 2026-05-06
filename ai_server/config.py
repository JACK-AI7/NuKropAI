import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Project ---
    PROJECT_NAME = "NuKropAI-Enterprise"
    VERSION = "2.0.0"
    
    # --- Security ---
    API_KEY = os.getenv("AI_API_KEY", "nukrop_secret_dev")
    API_KEY_NAME = "X-API-Key"
    
    # --- Hugging Face ---
    HF_TOKEN = os.getenv("HF_TOKEN")
    SPACE_ID = os.getenv("SPACE_ID", "jaswanthBreddy/nukropai-farming-ai")
    
    # --- Storage & Models ---
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    WEIGHTS_DIR = os.path.join(BASE_DIR, "weights")
    DATASET_DIR = os.path.join(BASE_DIR, "dataset", "captured")
    
    # --- Cache & Queues ---
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    
    # --- Databases ---
    QDRANT_HOST = os.getenv("QDRANT_HOST", ":memory:")
    
    # --- Model Paths ---
    MODELS = {
        "pest": os.path.join(WEIGHTS_DIR, "pest", "pest.pt"),
        "maize": os.path.join(WEIGHTS_DIR, "maize"),
        "mllm": os.path.join(WEIGHTS_DIR, "agri_mllm"),
        "crop": os.path.join(WEIGHTS_DIR, "crop_disease", "best_crop_disease_model.pt"),
        "leaf": os.path.join(WEIGHTS_DIR, "leaf_detection", "leaf.pt"),
        "soil": os.path.join(WEIGHTS_DIR, "soil_classification", "model.h5"),
        "npk": os.path.join(WEIGHTS_DIR, "npk_prediction", "model.joblib"),
    }

config = Config()
