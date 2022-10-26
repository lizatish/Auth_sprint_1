from typing import Optional

from db.cache import CacheStorage

cache: Optional[CacheStorage] = None


def get_redis_storage() -> CacheStorage:
    """Возвращает экземпляр redis."""
    return cache
