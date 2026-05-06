import torch
import os
import logging
import time
from .config import config

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.models = {}
        self.stats = {"requests": 0, "errors": 0, "start_time": time.time()}

    def load_all(self):
        """Load all configured models into memory"""
        for key, path in config.MODELS.items():
            if os.path.exists(path):
                try:
                    logger.info(f"🚚 Loading {key} from {path}...")
                    self.models[key] = self._load_single(key, path)
                    logger.info(f"✅ {key} loaded successfully.")
                except Exception as e:
                    logger.error(f"❌ Failed to load {key}: {e}")
                    self.stats["errors"] += 1
            else:
                logger.warning(f"⚠️ {key} weights missing at {path}")

    def _load_single(self, key, path):
        if key == "pest":
            from ultralytics import YOLO
            return YOLO(path)
        
        elif key == "leaf":
            from ultralytics import YOLO
            return YOLO(path)
            
        elif key == "maize":
            from transformers import AutoFeatureExtractor, AutoModelForImageClassification
            return {
                "extractor": AutoFeatureExtractor.from_pretrained(path),
                "model": AutoModelForImageClassification.from_pretrained(path)
            }
            
        elif key == "mllm":
            from transformers import AutoProcessor, AutoModelForVision2Seq
            return {
                "processor": AutoProcessor.from_pretrained(path),
                "model": AutoModelForVision2Seq.from_pretrained(path, low_cpu_mem_usage=True)
            }
            
        elif key == "crop":
            import timm
            model = timm.create_model('efficientnet_b3', pretrained=False, num_classes=38)
            model.load_state_dict(torch.load(path, map_location='cpu'))
            model.eval()
            return model
            
        elif key == "soil":
            import tensorflow as tf
            return tf.keras.models.load_model(path)
            
        elif key == "npk":
            import joblib
            return joblib.load(path)
            
        return None

    def get_model(self, key):
        return self.models.get(key)

manager = ModelManager()
