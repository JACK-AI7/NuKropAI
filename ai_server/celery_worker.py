from celery import Celery
import os
from .config import config

celery_app = Celery(
    "nukrop_tasks",
    broker=config.CELERY_BROKER,
    backend=config.CELERY_BACKEND
)

@celery_app.task
def process_mllm_task(image_path, prompt):
    """Background task for heavy MLLM analysis"""
    # This would run in a separate worker process
    return f"Completed background analysis for prompt: {prompt}"

@celery_app.task
def generate_regional_forecast_task(lat, lon):
    """Background task for generating complex forecasts"""
    # Simulate heavy calculation
    return {"status": "success", "lat": lat, "lon": lon}
