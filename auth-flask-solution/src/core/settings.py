import os
from functools import lru_cache
from datetime import timedelta
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""

    SECRET_KEY: str
    STATIC_FOLDER: str = 'static'
    TEMPLATES_FOLDER: str = 'templates'

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'auth'

    # Настройки Redis
    CACHE_HOST: str = '127.0.0.1'
    CACHE_PORT: int = 6379
    CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC: int = timedelta(hours=1).seconds
    CACHE_REFRESH_TOKEN_EXPIRED_SEC: int = timedelta(days=30).seconds
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

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str


class DevSettings(Settings):
    """Настройки для разработки приложения;"""

    FLASK_ENV: str = 'development'
    DEBUG: bool = True
    TESTING: bool = True

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../../.env.local'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """Возвращает настройки тестов."""
    return DevSettings()
