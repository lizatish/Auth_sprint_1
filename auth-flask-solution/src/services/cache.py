from db.redis import CacheStorage


class CacheService:
    """Сервис кеширования."""

    def __init__(self, storage: CacheStorage):
        """Инициализация сервиса."""
        self.db = storage

    def get(self, key: str) -> str:
        """Возвращает элементы по ключу."""
        return self.db.get(key)

    def set(self, key: str, value: str, expire: int) -> str:
        """Записывает ключ для хранения значения."""
        return self.db.set(key, value, expire)

    def lrange(self, key: str, start: int, stop: int) -> list:
        """Возвращает диапазон значений, лежащих по ключу."""
        return self.db.lrange(key, start, stop)

    def lpush(self, key: str, *elements: list[str]) -> int:
        """Кладет элемент в список по ключу в начало очереди."""
        return self.db.lpush(key, *elements)

    def expire(self, key: str, seconds: int) -> bool:
        """Задает время, после которого ключ станет невалидным."""
        return self.db.expire(key, seconds)
