import os
import torch
from transformers import pipeline, AutoModelForImageClassification, AutoFeatureExtractor, AutoModelForCausalLM, AutoTokenizer, AutoProcessor, AutoModelForSpeechSeq2Seq

# --- PRODUCTION MODELS LIST ---
VISION_MODEL = "linkanm/plant-disease-image-classification-vision-transformer"
VOICE_MODEL = "openai/whisper-tiny"
TEXT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def download_all_models():
    print("⏳ PRE-INSTALLING MULTI-MODE MODELS INTO ROOT CACHE...")
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1" # Makes download 3x faster

    # 1. PLANT DISEASE VISION MODE
    print("\n🌿 Mode 1: Installing Vision Crop Engine...")
    AutoModelForImageClassification.from_pretrained(VISION_MODEL)
    AutoFeatureExtractor.from_pretrained(VISION_MODEL)

    # 2. VOICE-FIRST TRANSCRIBER MODE (Hindi/Telugu/English support natively)
    print("\n🎙️ Mode 2: Installing Multilingual Whisper Audio...")
    AutoModelForSpeechSeq2Seq.from_pretrained(VOICE_MODEL)
    AutoProcessor.from_pretrained(VOICE_MODEL)

    # 3. LOCAL LLM OFFLINE CHATBOT (No external API needed)
    print("\n🤖 Mode 3: Installing TinyLlama Agronomy Brain...")
    AutoModelForCausalLM.from_pretrained(TEXT_MODEL)
    AutoTokenizer.from_pretrained(TEXT_MODEL)

    print("\n✅ ALL ADVANCED MODES DOWNLOADED AND READY FOR DEPLOYMENT!")

if __name__ == "__main__":
    download_all_models()