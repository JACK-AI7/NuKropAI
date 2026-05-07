"""GPU utilities for NuKropAI — safe VRAM management and device detection."""

import gc
import logging

logger = logging.getLogger("nukropai.gpu")


def get_device():
    """Return the best available device: cuda, mps, or cpu."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def get_vram_gb() -> float:
    """Return available VRAM in GB; returns 0 if no GPU is found."""
    try:
        import torch
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            return props.total_memory / (1024 ** 3)
    except Exception:
        pass
    return 0.0


def safe_empty_cache():
    """Release GPU cache and run garbage collection."""
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
    except Exception as e:
        logger.warning(f"Could not clear CUDA cache: {e}")


def should_use_4bit() -> bool:
    """
    Decide if 4-bit quantization should be used.
    - T4 (16 GB) and below → always use 4-bit to avoid OOM.
    - A100 (40+ GB) → optional, defaulting True for batch-safety.
    """
    vram = get_vram_gb()
    if vram == 0:
        return False   # CPU mode — no quantization
    return True        # use 4-bit on all GPU tiers


def log_gpu_status():
    """Log current GPU memory usage."""
    try:
        import torch
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated(0) / (1024 ** 2)
            reserved = torch.cuda.memory_reserved(0) / (1024 ** 2)
            total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 2)
            logger.info(
                f"GPU memory — Allocated: {allocated:.0f}MB | "
                f"Reserved: {reserved:.0f}MB | Total: {total:.0f}MB"
            )
        else:
            logger.info("Running on CPU — no GPU detected.")
    except Exception as e:
        logger.warning(f"Could not read GPU status: {e}")
