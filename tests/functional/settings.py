import logging
from functools import lru_cache

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """Базовые тестовые настройки."""

    # Настройки Flask
    TESTING: bool = True
    SECRET_KEY: str = 'secret-key'
    FLASK_ENV: str = 'test_production'

    # Настройки логирования
    LOG_LEVEL: int = logging.DEBUG

    # Настройки Redis
    CACHE_PORT: int = 6379
    CACHE_HOST: str

    # Настройки Postgres
    POSTGRES_DB_NAME: str = 'postgres'
    POSTGRES_DB_USER: str = 'postgres'
    POSTGRES_DB_PASSWORD: str = 'postgres'
    POSTGRES_DB_HOST: str = 'postgres'
    POSTGRES_DB_PORT: int = 5432
    JWT_ACCESS_TOKEN_EXPIRES: int = 300000
    
    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int

class TestSettingsDocker(TestSettings):
    """Тестовые настройки для развертки приложения через docker."""

    # Настройки Redis
    CACHE_HOST: str = 'test_auth_redis'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    # Настройки Postgres
    POSTGRES_DB_HOST: str = 'test_auth_postgres'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


class TestSettingsLocal(TestSettings):
    """Тестовые настройки для развертки приложения локально."""

    # Настройки Redis
    CACHE_HOST: str = 'localhost'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    # Настройки Postgres
    POSTGRES_DB_HOST: str = 'localhost'

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../.env.local'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> TestSettings:
    """Возвращает настройки тестов."""
    return TestSettingsLocal()
