"""
ModelManager — singleton that handles dynamic model loading/unloading
with VRAM safety, 4-bit quantization, and CPU fallback.
"""

import logging

from config import MODEL_REGISTRY
from utils.gpu_utils import safe_empty_cache, should_use_4bit, log_gpu_status

logger = logging.getLogger("nukropai.model_manager")


class ModelManager:
    """Loads and unloads one VL model at a time to prevent OOM."""

    def __init__(self):
        self.loaded_model = None
        self.loaded_processor = None
        self.current_name = None

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def load_model(self, model_name: str) -> None:
        """Load a model by registry name; skip if already loaded."""
        if self.current_name == model_name:
            logger.info(f"Model '{model_name}' already loaded — skipping.")
            return

        self.unload_model()
        self._load(model_name)

    def unload_model(self) -> None:
        """Unload the current model and free GPU memory."""
        if self.loaded_model is None:
            return

        logger.info(f"Unloading model '{self.current_name}'…")
        try:
            del self.loaded_model
            del self.loaded_processor
        except Exception:
            pass

        self.loaded_model = None
        self.loaded_processor = None
        self.current_name = None
        safe_empty_cache()
        logger.info("Model unloaded and cache cleared.")

    def get_model(self):
        return self.loaded_model

    def get_processor(self):
        return self.loaded_processor

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _load(self, model_name: str) -> None:
        """Internal: load model from Hugging Face Hub with error handling."""
        import torch
        from transformers import AutoProcessor, AutoModelForImageTextToText

        model_id = MODEL_REGISTRY.get(model_name)
        if not model_id:
            raise ValueError(f"Unknown model name: '{model_name}'. "
                             f"Available: {list(MODEL_REGISTRY.keys())}")

        logger.info(f"Loading model '{model_name}' from '{model_id}'…")

        try:
            processor = AutoProcessor.from_pretrained(
                model_id,
                trust_remote_code=True,
            )

            load_kwargs = {
                "device_map": "auto",
                "torch_dtype": torch.float16,
                "trust_remote_code": True,
            }

            use_4bit = should_use_4bit()
            if use_4bit:
                try:
                    from transformers import BitsAndBytesConfig
                    load_kwargs["quantization_config"] = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_use_double_quant=True,
                        bnb_4bit_quant_type="nf4",
                    )
                    logger.info("4-bit quantization enabled (BitsAndBytes NF4).")
                except ImportError:
                    logger.warning("bitsandbytes not found — loading in fp16.")

            model = AutoModelForImageTextToText.from_pretrained(
                model_id,
                **load_kwargs,
            )
            model.eval()

            self.loaded_model = model
            self.loaded_processor = processor
            self.current_name = model_name

            log_gpu_status()
            logger.info(f"Model '{model_name}' ready.")

        except Exception as e:
            safe_empty_cache()
            logger.error(f"Failed to load model '{model_name}': {e}")
            raise RuntimeError(f"Model load failed for '{model_name}': {e}") from e


model_manager = ModelManager()
