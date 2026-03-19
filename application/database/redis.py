from redis.asyncio import Redis

from application.config import settings


class RedisRepository:
    def __init__(self, url: str):
        self.redis = Redis.from_url(url)
        self.TTL = settings.REDIS_TTL * 60

    def _decode_redis_hash(self, data: dict):
        return {k.decode(): v.decode() for k, v in data.items()}

    async def add_item(self, name: str, mapping: dict):
        await self.redis.hset(name=name, mapping=mapping)
        await self.redis.expire(name, self.TTL)

    async def get_item(self, name: str):
        data = await self.redis.hgetall(name=name)
        if data:
            return self._decode_redis_hash(data)
        return None

    async def delete_item(self, name: str):
        await self.redis.delete(name)


cache = RedisRepository(url=settings.REDIS_URL)
