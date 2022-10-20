import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""
    SECRET_KEY: str
    SESSION_COOKIE_NAME: str
    STATIC_FOLDER: str = 'static'
    TEMPLATES_FOLDER: str = 'templates'

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'auth'

    # Настройки Redis
    CACHE_HOST: str = 'redis'
    CACHE_PORT: int = 6379

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


class ProdSettings(Settings):
    FLASK_ENV: str = 'production'
    DEBUG: bool = False
    TESTING: bool = False
    DATABASE_URI: str


class DevSettings(Settings):
    FLASK_ENV: bool = 'development'
    DEBUG: bool = True
    TESTING: bool = True
    DATABASE_URI: str


@lru_cache()
def get_dev_settings():
    """Возвращает настройки для тестирования."""
    return DevSettings()


@lru_cache()
def get_prod_settings():
    """Возвращает настройки для тестирования."""
    return ProdSettings()
