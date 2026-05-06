import os
import shutil
from huggingface_hub import hf_hub_download, snapshot_download
from .config import config

HF_TOKEN = config.HF_TOKEN

def download_pest():
    print("⬇️ Downloading Pest Detection (YOLO11s)...")
    from ultralytics import YOLO
    model = YOLO("underdogquality/yolo11s-pest-detection")
    os.makedirs(os.path.dirname(config.MODELS["pest"]), exist_ok=True)
    model.save(config.MODELS["pest"])

def download_maize():
    print("⬇️ Downloading Maize Disease Classification...")
    snapshot_download(
        repo_id="muAtarist/maize_disease_model",
        local_dir=config.MODELS["maize"],
        token=HF_TOKEN,
        ignore_patterns=["*.msgpack", "flax_model*", "tf_model*", "rust_model*"],
    )

def download_mllm():
    print("⬇️ Downloading Agricultural MLLM (SpaceLLaVA 2B)...")
    snapshot_download(
        repo_id="remyxai/SpaceLLaVA", 
        local_dir=config.MODELS["mllm"],
        token=HF_TOKEN,
        ignore_patterns=["*.msgpack", "flax_model*", "tf_model*", "rust_model*", "*.ot"],
    )

def download_crop():
    print("⬇️ Downloading General Crop Disease (EfficientNet)...")
    os.makedirs(os.path.dirname(config.MODELS["crop"]), exist_ok=True)
    hf_hub_download(
        repo_id="VisionaryQuant/5_Crop_Disease_Detection",
        filename="best_crop_disease_model.pt",
        local_dir=os.path.dirname(config.MODELS["crop"]),
        token=HF_TOKEN
    )

def download_leaf():
    print("⬇️ Downloading Leaf Detection (YOLOv8)...")
    from ultralytics import YOLO
    model = YOLO("foduucom/plant-leaf-detection-and-classification")
    os.makedirs(os.path.dirname(config.MODELS["leaf"]), exist_ok=True)
    model.save(config.MODELS["leaf"])

def download_soil():
    print("⬇️ Downloading Soil Classification (TensorFlow)...")
    os.makedirs(os.path.dirname(config.MODELS["soil"]), exist_ok=True)
    hf_hub_download(
        repo_id="Ben041/soil-type-classifier",
        filename="model.h5",
        local_dir=os.path.dirname(config.MODELS["soil"]),
        token=HF_TOKEN
    )

def download_npk():
    print("⬇️ Downloading NPK Recommendation (Scikit-learn)...")
    os.makedirs(os.path.dirname(config.MODELS["npk"]), exist_ok=True)
    hf_hub_download(
        repo_id="GodfreyOwino/NPK_needs_mode2",
        filename="model.joblib",
        local_dir=os.path.dirname(config.MODELS["npk"]),
        token=HF_TOKEN
    )

if __name__ == "__main__":
    print("=== NuKropAI Weight Downloader ===")
    tasks = [
        download_pest, download_maize, download_mllm, 
        download_crop, download_leaf, download_soil, download_npk
    ]
    for task in tasks:
        try:
            task()
        except Exception as e:
            print(f"❌ Task failed: {e}")
    print("=== Download complete ===")
