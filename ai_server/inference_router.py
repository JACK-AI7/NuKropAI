"""
InferenceRouter — runs model inference with safe error handling and
proper Qwen2.5-VL message formatting.
"""

import logging
from pathlib import Path

from PIL import Image
from model_manager import model_manager

logger = logging.getLogger("nukropai.inference")


class InferenceRouter:
    """Execute multimodal inference using the currently loaded model."""

    def run(
        self,
        model_name: str,
        image_path: str,
        prompt: str,
        system_prompt: str = "",
        max_new_tokens: int = 512,
    ) -> str:
        """
        Load model, run inference, return decoded text.
        Falls back to a structured error string on failure.
        """
        try:
            import torch

            model_manager.load_model(model_name)
            model = model_manager.get_model()
            processor = model_manager.get_processor()

            image = Image.open(image_path).convert("RGB")

            # Build Qwen2.5-VL compatible message format
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text",  "text": prompt},
                ],
            })

            # Attempt Qwen chat template; fall back to plain processor
            try:
                text_input = processor.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                )
                inputs = processor(
                    text=[text_input],
                    images=[image],
                    return_tensors="pt",
                )
            except Exception:
                inputs = processor(
                    images=image,
                    text=prompt,
                    return_tensors="pt",
                )

            # Move all tensors to the model's device
            device = next(model.parameters()).device
            inputs = {
                k: v.to(device) if hasattr(v, "to") else v
                for k, v in inputs.items()
            }

            with torch.inference_mode():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    temperature=1.0,
                    repetition_penalty=1.1,
                )

            # Decode only the newly generated tokens
            input_len = inputs["input_ids"].shape[1]
            new_tokens = output_ids[:, input_len:]
            result = processor.batch_decode(
                new_tokens,
                skip_special_tokens=True,
            )[0].strip()

            logger.info(f"Inference complete — {len(result)} chars generated.")
            return result

        except Exception as e:
            logger.error(f"Inference failed for model '{model_name}': {e}")
            return (
                f"I was unable to analyze the image at this time. "
                f"Please try again or rephrase your question. (Error: {type(e).__name__})"
            )


inference_router = InferenceRouter()
