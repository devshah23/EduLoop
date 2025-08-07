from redis.asyncio import Redis
from os import getenv

REDIS_URL=getenv("REDIS_URL","redis://localhost:6379")

r=Redis.from_url(REDIS_URL,decode_responses=True)