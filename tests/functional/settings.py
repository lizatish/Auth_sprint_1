import logging
from functools import lru_cache

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """Тестовые настройки для развертки приложения."""
    # Настройки flask
    TESTING: bool = True
    SECRET_KEY: str = 'secret-key'
    FLASK_ENV: str = 'test_production'

    # Настройки логирования
    LOG_LEVEL: int = logging.DEBUG

    # Настройки Redis
    CACHE_HOST: str = 'test-auth-redis'
    CACHE_PORT: int = 6379

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://test-auth_postgres'


@lru_cache()
def get_settings():
    """Возвращает настройки тестов."""
    return TestSettings()
