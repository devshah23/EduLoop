from redis.asyncio import Redis
from os import getenv

REDIS_HOST=getenv("REDIS_HOST", "localhost")
REDIS_PORT=int(getenv("REDIS_PORT", 6379))

r = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True  
)
