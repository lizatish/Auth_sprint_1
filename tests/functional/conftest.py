import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncIterator

import aioredis
import psycopg2
import pytest
import pytest_asyncio
from aioredis import Redis
from flask import Flask
from flask.testing import FlaskClient
from psycopg2._psycopg import connection, cursor
from psycopg2.extras import DictCursor

from core.app_factory import create_app
from db import redis
from tests.functional.settings import get_settings
from tests.functional.testdata.login import test_data_for_success_login_user
from tests.functional.testdata.postgresdata import users_data


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
    """Фикстура главного приложения."""
    settings = get_settings()
    app = create_app(settings)
    yield app


@pytest.fixture()
def auth_api_client(app: Flask, redis_pool: Redis) -> FlaskClient:
    """Фикстура апи-клиента."""
    redis.cache = redis_pool
    yield app.test_client()


@pytest.fixture(scope="session")
def db_cursor(db_connection) -> cursor:
    """Фикстура курсоры бд."""
    curs_postgres = db_connection.cursor()

    f_str = "INSERT INTO \"public\".user (id, username, password, role) values (%s, %s, %s, %s)"
    curs_postgres.executemany(f_str, users_data)

    yield curs_postgres
    curs_postgres.execute(f"DELETE FROM public.user;")
    db_connection.commit()


@pytest.fixture(scope="session")
def db_connection(app: Flask) -> connection:
    """Фикстура подключения к бд."""
    dsl = {
        'dbname': app.config['POSTGRES_DB_NAME'],
        'user': app.config['POSTGRES_DB_USER'],
        'password': app.config['POSTGRES_DB_PASSWORD'],
        'host': app.config['POSTGRES_DB_HOST'],
        'port': app.config['POSTGRES_DB_PORT'],
    }
    print(dsl)
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield pg_conn
    pg_conn.close()
