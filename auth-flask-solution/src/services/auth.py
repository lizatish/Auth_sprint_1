from functools import lru_cache

from db.cache import CacheStorage
from db.redis import get_redis_storage
from services.cache import CacheService


class AuthService:
    """Сервис авторизации и аутентификации."""

    def __init__(self, cache_storage: CacheStorage):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)

    def register(self):
        pass

    def login(self):
        pass

    def logout(self):
        pass


@lru_cache()
def get_auth_service() -> AuthService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    cache_storage: CacheStorage = get_redis_storage()
    return AuthService(cache_storage)
