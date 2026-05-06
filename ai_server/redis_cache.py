import redis.asyncio as redis
import json
import logging
import hashlib
from .config import config

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.url = config.REDIS_URL
        self.client = None

    async def connect(self):
        if self.url:
            try:
                self.client = redis.from_url(self.url, decode_responses=True)
                await self.client.ping()
                logger.info("✅ Redis Connected")
            except Exception as e:
                logger.error(f"❌ Redis Connection Failed: {e}")

    async def get_cached_result(self, image_bytes, prefix="scan"):
        if not self.client: return None
        img_hash = hashlib.md5(image_bytes).hexdigest()
        cached = await self.client.get(f"{prefix}:{img_hash}")
        return json.loads(cached) if cached else None

    async def cache_result(self, image_bytes, result, prefix="scan", ex=3600):
        if not self.client: return
        img_hash = hashlib.md5(image_bytes).hexdigest()
        await self.client.set(f"{prefix}:{img_hash}", json.dumps(result), ex=ex)

    async def close(self):
        if self.client:
            await self.client.close()

redis_cache = RedisCache()
