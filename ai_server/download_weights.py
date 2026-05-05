from ultralytics import YOLO
from huggingface_hub import hf_hub_download, snapshot_download
import os

def download_models():
    print("Downloading Farming AI models...")
    
    # 1. Pest Detection (YOLO11)
    print("Downloading YOLO11 Pest Detector...")
    try:
        # Load the model directly from the Hub
        model_pest = YOLO("underdogquality/yolo11s-pest-detection")
    except Exception as e:
        print(f"Error downloading YOLO11: {e}")

    # 2. Maize Disease
    print("Downloading Maize Disease Detection...")
    try:
        hf_hub_download(repo_id="muAtarist/maize_disease_model", filename="model.safetensors")
    except Exception as e:
        print(f"Error downloading Maize model: {e}")

    # 3. PlantNet
    print("Downloading PlantNet-Disease-Detection...")
    try:
        snapshot_download(repo_id="prof-freakenstein/plantnet-disease-detection")
    except Exception as e:
        print(f"Error downloading PlantNet: {e}")

    # 4. Crop Recommendation
    print("Downloading Crop Recommendation model...")
    try:
        hf_hub_download(repo_id="randalakab/Crop-recommendation", filename="model.pkl")
    except Exception as e:
        print(f"Error downloading Crop Recommendation: {e}")

    print("All models downloaded/verified.")

if __name__ == "__main__":
    download_models()
