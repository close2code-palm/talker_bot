from typing import Set, List

from redis.asyncio import Redis


class Repository:

    def __init__(self, conn: Redis):
        self._conn = conn

    async def limit_reached(self, tg_id: str, limit: int = 15) -> bool:
        count = await self._conn.scard(tg_id)
        if count < limit:
            return False
        return True

    async def save_phrase(self, tg_id: str, phrase: str):
        """Store phrase for new or existing users set."""
        await self._conn.sadd(tg_id, phrase)

    async def get_phrases(self, tg_id: str) -> List[str]:
        """Gets all phrases stored for user"""
        binary_phrases = await self._conn.smembers(tg_id)
        return list(map(bytes.decode, binary_phrases))

    async def remove_phrase(self, tg_id: str, phrase: str):
        await self._conn.srem(tg_id, phrase)
