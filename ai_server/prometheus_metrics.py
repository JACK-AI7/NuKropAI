from prometheus_fastapi_instrumentator import Instrumentator
import logging

logger = logging.getLogger(__name__)

def setup_metrics(app):
    """Expose /metrics endpoint for Prometheus monitoring"""
    try:
        Instrumentator().instrument(app).expose(app)
        logger.info("✅ Prometheus Metrics Initialized")
    except Exception as e:
        logger.error(f"❌ Metrics Init Failed: {e}")
