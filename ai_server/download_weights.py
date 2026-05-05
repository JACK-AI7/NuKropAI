from ultralytics import YOLO
import os

def download_model():
    print("Downloading YOLOv8 model weights...")
    model = YOLO("yolov8n.pt")
    print("Download complete.")

if __name__ == "__main__":
    download_model()
