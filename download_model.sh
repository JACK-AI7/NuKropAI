#!/bin/bash

echo "========================================"
echo "KropAI - Download On-Device ML Model"
echo "========================================"
echo ""

MODEL_DIR="assets/models"
MODEL_FILE="${MODEL_DIR}/crop_disease_model.tflite"
LABELS_FILE="${MODEL_DIR}/crop_disease_labels.txt"

echo "📁 Creating models directory..."
mkdir -p "$MODEL_DIR"

echo ""
echo "📥 Downloading TFLite model..."
# Download a lightweight MobileNetV2-based crop disease classification model
# This is a community-trained model for common plant diseases
curl -L -o "$MODEL_FILE" "https://github.com/akkadia-org/plant-disease-detection-models/raw/main/model.tflite" 2>/dev/null || {
    echo "⚠️  Primary download failed. Trying alternative source..."
    curl -L -o "$MODEL_FILE" "https://tfhub.dev/google/lite-model/imagenet/mobilenet_v2_dims_224/feature_vector/2?lite-format=tflite"
}

if [ -f "$MODEL_FILE" ]; then
    echo "✅ Model downloaded: $(ls -lh "$MODEL_FILE" | awk '{print $5}')"
else
    echo "❌ Failed to download model. Please download manually and place at: $MODEL_FILE"
    echo "   Recommended model: PlantVillage dataset trained MobileNetV2 (~16MB)"
    echo "   Or run: flutter pub add tflite && add model to assets/models/"
fi

echo ""
echo "📝 Creating labels file..."
cat > "$LABELS_FILE" << 'EOF'
Apple_Scab
Apple_Black_Rot
Apple_Cedar_Rust
Apple_Healthy
Blueberry_Healthy
Cherry_Powdery_Mildew
Cherry_Healthy
Corn_Cercospora_Leaf_Spot
Corn_Common_Rust
Corn_Northern_Leaf_Blight
Corn_Healthy
Grape_Black_Rot
Grape_Esca
Grape_Leaf_Blight
Grape_Healthy
Orange_Huanglongbing
Peach_Bacterial_Spot
Peach_Healthy
Bell_Pepper_Bacterial_Spot
Bell_Pepper_Healthy
Potato_Early_Blight
Potato_Late_Blight
Potato_Healthy
Raspberry_Healthy
Soybean_Healthy
Squash_Powdery_Mildew
Strawberry_Leaf_Scorch
Strawberry_Healthy
Tomato_Bacterial_Spot
Tomato_Early_Blight
Tomato_Late_Blight
Tomato_Leaf_Mold
Tomato_Septoria_Leaf_Spot
Tomato_Spider_Mites
Tomato_Target_Spot
Tomato_Mosaic_Virus
Tomato_Yellow_Leaf_Curl_Virus
Tomato_Healthy
Rice_Blast
Rice_Bacterial_Blight
Rice_Tungro
Rice_Healthy
Wheat_Rust
Wheat_Healthy
Soil_Alluvial
Soil_Black
Soil_Red
Soil_Laterite
EOF

echo "✅ Labels created: ${LABELS_FILE}"
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To use on-device AI:"
echo "1. Restart your Flutter app"
echo "2. The model will load automatically on first scan"
echo ""
echo "Note: The model file should ideally be smaller than 50MB for fast app startup."
echo "You can replace it with a custom-trained model for your specific crops."
echo ""
