import os

APP_NAME = "NuKropAI"
APP_VERSION = "1.0.0"

DEFAULT_MODEL = "qwen_vl"

USE_4BIT = True

MODEL_REGISTRY = {
    "qwen_vl": os.getenv(
        "QWEN_VL_MODEL",
        "Qwen/Qwen2.5-VL-7B-Instruct"
    ),

    "phi4_mm": os.getenv(
        "PHI4_MM_MODEL",
        "microsoft/Phi-4-multimodal-instruct"
    ),

    "llama_vision": os.getenv(
        "LLAMA_VISION_MODEL",
        "meta-llama/Llama-3.2-11B-Vision-Instruct"
    ),

    "agrichat": os.getenv("AGRICHAT_MODEL", ""),
    "agrigpt_vl": os.getenv("AGRIGPT_VL_MODEL", ""),
    "agrim_llm": os.getenv("AGRIM_LLM_MODEL", ""),
    "agrillava": os.getenv("AGRILLAVA_MODEL", ""),
}
