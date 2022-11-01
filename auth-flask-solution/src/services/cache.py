from flask import current_app

from db.redis import CacheStorage


class CacheService:
    """Сервис кеширования."""

    def __init__(self, storage: CacheStorage):
        """Инициализация сервиса."""
        self.db = storage

    def set_revoked_access_token(self, user_id: str, revoked_access_token: str):
        return self.db.set(
            f"access_{user_id}",
            revoked_access_token,
            current_app.config['CACHE_REVOKED_ACCESS_TOKEN_EXPIRED_SEC'],
        )

    def set_refresh_token(self, user_id: str, refresh_token: str):
        return self.db.set(
            f"refresh_{user_id}",
            refresh_token,
            current_app.config['CACHE_REFRESH_TOKEN_EXPIRED_SEC'],
        )

    def get_revoked_access_token(self, user_id: str) -> str:
        return self.db.get(f"access_{user_id}")

    def get_refresh_token(self, user_id: str) -> str:
        return self.db.get(f"refresh_{user_id}")
