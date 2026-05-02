@echo off
echo ========================================
echo KropAI - Download On-Device ML Model
echo ========================================
echo.

set "MODEL_DIR=mobile\assets\models"
set "MODEL_FILE=%MODEL_DIR%\crop_disease_model.tflite"
set "LABELS_FILE=%MODEL_DIR%\crop_disease_labels.txt"

echo Creating models directory...
if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"

echo.
echo Downloading TFLite model...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/akkadia-org/plant-disease-detection-models/raw/main/model.tflite' -OutFile '%MODEL_FILE%' -UseBasicParsing" 2>nul
if not exist "%MODEL_FILE%" (
    echo Primary download failed, trying alternative...
    powershell -Command "Invoke-WebRequest -Uri 'https://tfhub.dev/google/lite-model/imagenet/mobilenet_v2_dims_224/feature_vector/2?lite-format=tflite' -OutFile '%MODEL_FILE%' -UseBasicParsing" 2>nul
)

if exist "%MODEL_FILE%" (
    echo Model downloaded successfully
) else (
    echo Failed to download model automatically.
    echo Please download manually from:
    echo   https://github.com/akkadia-org/plant-disease-detection-models/
    echo And place at: %MODEL_FILE%
)

echo.
echo Creating labels file...
(
echo Apple_Scab
echo Apple_Black_Rot
echo Apple_Cedar_Rust
echo Apple_Healthy
echo Blueberry_Healthy
echo Cherry_Powdery_Mildew
echo Cherry_Healthy
echo Corn_Cercospora_Leaf_Spot
echo Corn_Common_Rust
echo Corn_Northern_Leaf_Blight
echo Corn_Healthy
echo Grape_Black_Rot
echo Grape_Esca
echo Grape_Leaf_Blight
echo Grape_Healthy
echo Orange_Huanglongbing
echo Peach_Bacterial_Spot
echo Peach_Healthy
echo Bell_Pepper_Bacterial_Spot
echo Bell_Pepper_Healthy
echo Potato_Early_Blight
echo Potato_Late_Blight
echo Potato_Healthy
echo Raspberry_Healthy
echo Soybean_Healthy
echo Squash_Powdery_Mildew
echo Strawberry_Leaf_Scorch
echo Strawberry_Healthy
echo Tomato_Bacterial_Spot
echo Tomato_Early_Blight
echo Tomato_Late_Blight
echo Tomato_Leaf_Mold
echo Tomato_Septoria_Leaf_Spot
echo Tomato_Spider_Mites
echo Tomato_Target_Spot
echo Tomato_Mosaic_Virus
echo Tomato_Yellow_Leaf_Curl_Virus
echo Tomato_Healthy
echo Rice_Blast
echo Rice_Bacterial_Blight
echo Rice_Tungro
echo Rice_Healthy
echo Wheat_Rust
echo Wheat_Healthy
echo Soil_Alluvial
echo Soil_Black
echo Soil_Red
echo Soil_Laterite
) > "%LABELS_FILE%"

echo Labels created: %LABELS_FILE%
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. flutter pub get
echo 2. flutter run
echo.
pause
