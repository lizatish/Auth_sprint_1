import os
from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""

    # Базовые настройки приложения
    SECRET_KEY: str

    # Настройки аутентификации
    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'auth'

    # Настройки Redis
    CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC: int = timedelta(hours=1).seconds
    CACHE_REFRESH_TOKEN_EXPIRED_SEC: int = timedelta(days=30).seconds
    CACHE_HOST: str
    CACHE_PORT: int = 6379

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


class ProdSettings(Settings):
    """Настройки для развертки приложения."""

    FLASK_ENV: str = 'production'
    DEBUG: bool = False
    TESTING: bool = False

    # Настройки Redis
    CACHE_HOST: str = 'auth_redis'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://auth_postgres'


class DevSettings(Settings):
    """Настройки для разработки приложения;"""

    FLASK_ENV: str = 'development'
    DEBUG: bool = True
    TESTING: bool = True

    # Настройки Redis
    CACHE_HOST: str = 'localhost'

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../../.env.local'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """Возвращает настройки тестов."""
    return ProdSettings()
