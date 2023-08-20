import pytest
import pytest_asyncio
from redis import asyncio

from src.polite_bot.services import Repository


@pytest_asyncio.fixture(name='redis_client')
async def fixture_redis_client():
    """Test connection provider."""
    redis = asyncio.Redis()
    try:
        yield Repository(redis)
    finally:
        await redis.close()


@pytest.mark.asyncio
async def test_add(redis_client: Repository):
    await redis_client.save_phrase('2', 'oki')
    saved = await redis_client.get_phrases('2')
    assert 'oki' in saved


