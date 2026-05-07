FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ai_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port
EXPOSE 7860

# Set env vars
ENV HOST=0.0.0.0
ENV PORT=7860
ENV PYTHONPATH=/app:/app/ai_server

# Command to run the FastAPI app
# We use ai_server.main:app because of the PYTHONPATH=/app setting
CMD ["uvicorn", "ai_server.main:app", "--host", "0.0.0.0", "--port", "7860"]
