"""Optional Redis cache for auth (e.g. user by sub) to reduce DB hits."""
import json
from typing import Any, Optional

_redis_client: Optional[Any] = None


def get_redis():
    """Return async Redis client if REDIS_URL is set; else None."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    try:
        from redis.asyncio import Redis
        from config.settings import REDIS_URL
        _redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
        return _redis_client
    except Exception:
        return None


async def get_user_cached(sub: str) -> Optional[dict]:
    """Get cached user dict by sub (username). Returns None on miss or if Redis unavailable."""
    redis = get_redis()
    if not redis:
        return None
    try:
        data = await redis.get(f"user:sub:{sub}")
        return json.loads(data) if data else None
    except Exception:
        return None


async def set_user_cached(sub: str, user_dict: dict, ttl_seconds: int = 300) -> None:
    """Cache user dict by sub. TTL default 5 minutes."""
    redis = get_redis()
    if not redis:
        return
    try:
        await redis.setex(
            f"user:sub:{sub}",
            ttl_seconds,
            json.dumps(user_dict, default=str),
        )
    except Exception:
        pass


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        try:
            await _redis_client.aclose()
        except Exception:
            pass
        _redis_client = None
