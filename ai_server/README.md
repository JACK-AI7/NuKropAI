---
title: NuKropAI Farming Multi-Model Server
emoji: 🌿
colorFrom: green
colorTo: lime
sdk: docker
app_port: 7860
pinned: true
---

# NuKropAI — Advanced Multi-Model Farming Server

This is a production-grade FastAPI server optimized for **Hugging Face Spaces**. it serves as the intelligent backend for the NuKropAI farming app, providing real-time diagnostics, pest detection, and agricultural advice.

## 🚀 Key Features
- **Multi-Model Routing**: Automatically selects the best model for the task (YOLO11, EfficientNet, TensorFlow).
- **Smart Failover**: Fallbacks to the **Agri-MLLM (SpaceLLaVA)** if specific classifiers have low confidence.
- **Hugging Face Native**: Built to run on HF Spaces with optional GPU support.
- **Agricultural Specialist APIs**: Dedicated endpoints for pests, soil, NPK, and general crop diseases.

## 🛠️ API Endpoints

### 🔍 Diagnostics
- **POST** `/analyze/crop`: Smart router for all crop diseases.
- **POST** `/detect/pest`: Specialized YOLO11 pest identification.
- **POST** `/classify/soil`: CNN-based soil type classification.
- **POST** `/analyze/agri-llava`: Conversational multimodal analysis.

### 📊 Agronomy & Recommendations
- **POST** `/recommend/npk`: Nutrient recommendation based on NPK/pH/Moisture.
- **POST** `/chat/agronomist`: Text-only agricultural expert chat.

## 📦 Deployment to Hugging Face
1. Create a [New Space](https://huggingface.co/new-space).
2. Choose **Docker**.
3. Upload this directory.
4. (Optional) Set `HF_TOKEN` in **Settings > Secrets** to download gated models.

## 📱 Mobile Connection
Set `aiServerUrl` in `mobile/lib/core/config/constants.dart` to your Space URL.
