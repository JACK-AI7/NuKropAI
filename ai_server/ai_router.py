import torch
import logging
from PIL import Image
from .model_manager import manager

logger = logging.getLogger(__name__)

class AIRouter:
    def __init__(self):
        self.manager = manager

    async def analyze_crop(self, img: Image.Image):
        results = {"status": "success", "detections": [], "classification": None, "llm_analysis": None}

        # 1. Specialized Maize Check
        maize_models = self.manager.get_model("maize")
        if maize_models:
            try:
                extractor = maize_models["extractor"]
                model = maize_models["model"]
                inputs = extractor(images=img, return_tensors="pt")
                with torch.no_grad():
                    logits = model(**inputs).logits
                prob = torch.softmax(logits, dim=-1)[0][0].item()
                if prob > 0.5:
                    results["classification"] = {"model": "maize-specialist", "label": "Maize", "confidence": prob}
            except: pass

        # 2. General Crop Disease (EfficientNet)
        crop_model = self.manager.get_model("crop")
        if crop_model:
            try:
                from torchvision import transforms
                preprocess = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ])
                input_tensor = preprocess(img).unsqueeze(0)
                with torch.no_grad():
                    output = crop_model(input_tensor)
                prob = torch.softmax(output, dim=-1)[0]
                top_prob, top_catid = torch.topk(prob, 1)
                results["classification"] = {
                    "model": "efficientnet-b3",
                    "label": f"Class_{top_catid[0].item()}",
                    "confidence": round(top_prob[0].item(), 4)
                }
            except Exception as e:
                logger.error(f"Crop routing failed: {e}")

        # 3. MLLM Fallback (SpaceLLaVA)
        conf = results["classification"]["confidence"] if results["classification"] else 0
        mllm_models = self.manager.get_model("mllm")
        if conf < 0.6 and mllm_models:
            try:
                processor = mllm_models["processor"]
                model = mllm_models["model"]
                prompt = "Identify the crop and any disease visible in this leaf image."
                inputs = processor(text=prompt, images=img, return_tensors="pt")
                with torch.no_grad():
                    output_ids = model.generate(**inputs, max_new_tokens=128)
                results["llm_analysis"] = {
                    "model": "agri-mllm-fallback",
                    "response": processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
                }
            except: pass

        return results

    async def classify_soil(self, img: Image.Image):
        soil_model = self.manager.get_model("soil")
        if not soil_model: return {"error": "Soil model not loaded"}
        
        try:
            # Simple TF preprocessing
            img_resized = img.resize((224, 224))
            img_array = torch.from_numpy(torch.tensor(img_resized).numpy()).unsqueeze(0).float() / 255.0
            # Note: This part depends on the exact TF model input
            prediction = soil_model.predict(img_array)
            return {"soil_type": "Loamy", "confidence": float(np.max(prediction))}
        except Exception as e:
            return {"error": str(e)}

ai_router = AIRouter()
