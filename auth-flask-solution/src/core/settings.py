import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Базовый класс конфигурации."""
    SECRET_KEY: str
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
    """Настройки для развертки приложения."""

    FLASK_ENV: str = 'production'
    DEBUG: bool = False
    TESTING: bool = False

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://auth_postgres'


class DevSettings(Settings):
    """Настройки для разработки приложения;"""

    FLASK_ENV: str = 'development'
    DEBUG: bool = True
    TESTING: bool = True

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI: str = ''

    class Config:
        """Дополнительные базовые настройки."""

        env_file = '../../.env.local'
        env_file_encoding = 'utf-8'
