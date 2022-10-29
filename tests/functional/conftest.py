import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncIterator

import aioredis
import pytest
import pytest_asyncio
from aioredis import Redis
from flask import Flask
from psycopg2.extras import DictCursor
import psycopg2
from core.app_factory import create_app
from db.db_factory import get_db
from db import redis
from tests.functional.settings import get_settings
from psycopg2 import extras
from flask_jwt_extended import create_access_token
from tests.functional.testdata.generate_tokens import users_data_for_tokens
from tests.functional.testdata.postgresdata import users_data
from flask_jwt_extended import JWTManager
from datetime import timedelta


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Фикстура главного цикла событий."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_pool(app: Flask) -> AsyncIterator[Redis]:
    """Фикстура соединения с redis."""
    pool = aioredis.from_url(
        f"redis://{app.config['CACHE_HOST']}:{app.config['CACHE_PORT']}", encoding="utf-8", decode_responses=True
    )
    yield pool
    await pool.close()


@pytest_asyncio.fixture
async def redis_flushall(redis_pool):
    """Фикстура, удаляющая кеш редиса."""
    await redis_pool.flushall()


@pytest_asyncio.fixture(scope="session")
def app() -> Flask:
    settings = get_settings()
    app = create_app(settings)
    yield app


@pytest.fixture(scope="session")
def db_cursor(db_connection):
    curs_postgres = db_connection.cursor()
    f_str = "INSERT INTO \"public\".user (id, username, password, role) values (%s, %s, %s, %s)"
    curs_postgres.executemany(f_str, users_data)
    yield curs_postgres
    curs_postgres.execute(f"DELETE FROM public.user;")
    db_connection.commit()


@pytest.fixture(scope="session")
def db_connection():
    dsl = {
        'dbname': 'auth_database', 'user': 'app_auth',
        'password': '123qwe_auth', 'host': 'localhost', 'port': 5434
    }
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield pg_conn
    pg_conn.close()


@pytest.fixture(scope="session")
def generate_access_token_for_user(app):
    result = {}
    with app.app_context():
        for item in users_data_for_tokens:
            result[item['username']] = create_access_token(identity=item)
    yield result

@pytest.fixture(scope="session")
def auth_api_client(app: Flask, redis_pool: Redis):
    """Фикстура апи-клиента."""
    redis.cache = redis_pool
    app = app.test_client()
    yield app
