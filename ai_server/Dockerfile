FROM python:3.10-slim

# --- System Dependencies ---
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Cache Config ---
ENV HF_HOME=/app/weights/hf_cache
ENV TRANSFORMERS_CACHE=/app/weights/hf_cache
ENV TORCH_HOME=/app/weights/torch_cache
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- Dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- Download Models at Build Time ---
# Ensure HF_TOKEN is set in Space secrets
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}
RUN python -m ai_server.download_weights

# --- Final Prep ---
RUN chmod +x startup.sh
EXPOSE 7860

CMD ["./startup.sh"]
