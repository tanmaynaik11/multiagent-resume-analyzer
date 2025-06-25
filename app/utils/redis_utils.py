from app.config import REDIS_HOST, REDIS_PORT
from app.utils.logger import get_logger
import redis, pickle

logger = get_logger("RedisUtils")
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def save_to_redis(key: str, value: dict):
    try:
        redis_client.set(key, pickle.dumps(value))
        logger.info(f"Saved to Redis: {key}")
    except Exception as e:
        logger.error(f"Failed saving to Redis: {e}")

def load_from_redis(key: str):
    try:
        data = redis_client.get(key)
        if data:
            logger.info(f"Loaded from Redis: {key}")
            return pickle.loads(data)
    except Exception as e:
        logger.error(f"Failed loading from Redis: {e}")
    return None
