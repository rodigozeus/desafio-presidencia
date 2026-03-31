import redis
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Redis connected")
except Exception:
    logger.warning("Redis not available, caching disabled")
    redis_client = None

def cache_get(key: str):
    if not redis_client:
        return None
    try:
        val = redis_client.get(key)
        return json.loads(val) if val else None
    except Exception:
        return None

def cache_set(key: str, value, ttl: int = settings.CACHE_TTL):
    if not redis_client:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass

def cache_delete_pattern(pattern: str):
    if not redis_client:
        return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
