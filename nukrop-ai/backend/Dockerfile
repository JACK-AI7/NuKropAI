FROM python:3.10-slim
WORKDIR /app

# Install system dependencies for OpenCV and audio processing
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory for caching
RUN mkdir -p /app/models

# Download models during build (optional - can be done at runtime)
# RUN python download_weights.py

# Expose port
EXPOSE 8080

# Start with model download and server
CMD ["sh", "-c", "python download_weights.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"]