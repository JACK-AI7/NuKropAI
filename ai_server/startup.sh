#!/bin/bash

# --- Start Background Services ---
echo "🚀 Starting Celery Worker..."
celery -A ai_server.celery_worker worker --loglevel=info &

echo "📈 Starting Monitoring (Flower)..."
celery -A ai_server.celery_worker flower --port=5555 &

# --- Start Main Application ---
echo "🌿 Starting NuKropAI Enterprise Server..."
python -m uvicorn ai_server.main:app --host 0.0.0.0 --port 7860 --workers 1
