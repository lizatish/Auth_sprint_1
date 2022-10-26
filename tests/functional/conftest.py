import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncIterator

import aioredis
import pytest
import pytest_asyncio
from aioredis import Redis
from flask import Flask

from core.app_factory import create_app
from db import redis
from tests.functional.settings import get_settings

conf = get_settings()


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Фикстура главного цикла событий."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_pool() -> AsyncIterator[Redis]:
    """Фикстура соединения с redis."""
    pool = aioredis.from_url(
        f"redis://{conf.CACHE_HOST}:{conf.CACHE_PORT}", encoding="utf-8", decode_responses=True
    )
    yield pool
    await pool.close()


@pytest_asyncio.fixture
async def redis_flushall(redis_pool):
    """Фикстура, удаляющая кеш редиса."""
    await redis_pool.flushall()


@pytest.fixture()
def app() -> Flask:
    settings_filename = 'tests.functional.settings.TestSettings'
    app = create_app(settings_filename)
    yield app


@pytest.fixture()
def auth_api_client(app: Flask, redis_pool: Redis):
    """Фикстура апи-клиента."""
    redis.cache = redis_pool
    yield app.test_client()
