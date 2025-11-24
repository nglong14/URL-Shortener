import redis
import json
from typing import Optional

# Initialize Redis client
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

def get_cache(key: str) -> Optional[dict]:
    """Get value from Redis cache"""
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except redis.ConnectionError:
        return None

def set_cache(key: str, value: dict, ttl: int = 3600) -> bool:
    """Set value in Redis cache with TTL (time to live in seconds)"""
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except redis.ConnectionError:
        return False

def delete_cache(key: str) -> bool:
    """Delete value from Redis cache"""
    try:
        redis_client.delete(key)
        return True
    except redis.ConnectionError:
        return False

def invalidate_user_urls_cache(user_id: int) -> bool:
    """Invalidate user's URLs cache when they create/update/delete a URL"""
    return delete_cache(f"user_urls:{user_id}")

def increment_clicks(short_code: str) -> int:
    """Increment click count in Redis for a short code"""
    try:
        key = f"clicks:{short_code}"
        return redis_client.incr(key)
    except redis.ConnectionError:
        return 0

def get_clicks(short_code: str) -> int:
    """Get click count from Redis"""
    try:
        key = f"clicks:{short_code}"
        clicks = redis_client.get(key)
        return int(clicks) if clicks else 0
    except redis.ConnectionError:
        return 0
