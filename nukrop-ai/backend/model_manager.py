import torch
import gc
from PIL import Image
import librosa
from transformers import (
    pipeline,
    AutoModelForImageClassification,
    AutoFeatureExtractor,
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoProcessor,
    AutoModelForSpeechSeq2Seq
)

class AI_Manager:
    _instance = None

    # Check if a GPU is available. Otherwise gracefully fall back to CPU
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Track what is currently active in Server RAM
    active_models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AI_Manager, cls).__new__(cls)
            cls.VISION_NAME = "linkanm/plant-disease-image-classification-vision-transformer"
            cls.VOICE_NAME = "openai/whisper-tiny"
            cls.TEXT_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        return cls._instance

    def _clear_vram(self):
        """Ultra-critical memory function: Prevents server crash!"""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # ==========================================
    # MODE 1: VISUAL LEAF SCANNER
    # ==========================================
    def scan_leaf_disease(self, image_file_bytes):
        if 'vision' not in self.active_models:
            print("📦 Loading Vision AI into RAM...")
            # We load dynamically into pipeline
            self.active_models['vision'] = pipeline(
                task="image-classification",
                model=self.VISION_NAME,
                device=0 if torch.cuda.is_available() else -1
            )

        # Inference Logic
        predictions = self.active_models['vision'](image_file_bytes)
        return {
            "disease": predictions[0]['label'],
            "confidence": round(predictions[0]['score'] * 100, 2)
        }

    # ==========================================
    # MODE 2: MULTILINGUAL VOICE CHAT TO TEXT
    # ==========================================
    def translate_audio_to_text(self, audio_file_path):
        if 'whisper' not in self.active_models:
            print("📦 Loading Whisper Voice AI into RAM...")
            self.active_models['whisper'] = pipeline(
                "automatic-speech-recognition",
                model=self.VOICE_NAME,
                torch_dtype=self.torch_dtype,
                device=0 if torch.cuda.is_available() else -1,
            )

        # Converts whatever audio format the app sends into NumPy text for PyTorch
        audio_numpy, rate = librosa.load(audio_file_path, sr=16000)

        result = self.active_models['whisper']({"array": audio_numpy, "sampling_rate": 16000})
        return result["text"]

    # ==========================================
    # MODE 3: TINY-LLM AGRONOMY BRAIN
    # ==========================================
    def agronomy_chat(self, user_prompt, chat_history_string):
        if 'llm' not in self.active_models:
            print("📦 Loading Offline Agri LLM into RAM...")
            self.active_models['llm'] = pipeline(
                "text-generation",
                model=self.TEXT_NAME,
                torch_dtype=self.torch_dtype,
                device_map="auto" # Handles GPU splitting if on bigger tiers
            )

        sys_prompt = f"System: You are an elite Y-Combinator farming AI.\nHistory: {chat_history_string}\nFarmer: {user_prompt}\nBot: "

        output = self.active_models['llm'](
            sys_prompt,
            max_new_tokens=150,
            temperature=0.3,
            do_sample=True,
            return_full_text=False
        )
        return output[0]['generated_text']

    # ==========================================
    # CLEANUP FOR SERVER LONGEVITY
    # ==========================================
    def kill_mode(self, mode_name):
        """Called by background workers after execution to free up memory"""
        if mode_name in self.active_models:
            del self.active_models[mode_name]
            self._clear_vram()
            print(f"🗑️ Cleaned {mode_name} from Memory!")

# Single Global Instance Export (like standard Enterprise configs)
ai_core = AI_Manager()