from functools import lru_cache
from flask_jwt_extended import create_access_token, create_refresh_token

from db.cache import CacheStorage
from db.redis import get_redis_storage
from models.db_models import User, db, Role
from services.cache import CacheService
from models.general import RoleType
from services.json import JsonService


class RolesService:
    """Сервис ролей."""

    def __init__(self, cache_storage: CacheStorage):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.db_connection = db

    @staticmethod
    def get_roles():
        """Получить все роли."""
        return Role.query.all()

    @staticmethod
    def get_role_by_id(role_id: str):
        """Получить роль по id"""
        try:
            return Role.query.get(role_id)
        except:
            return None

    def delete_role_by_id(self, role_id: str):
        """Удалить роль по id."""
        try:
            role = Role.query.get(role_id)
            self.db_connection.session.delete(role)
            self.db_connection.session.commit()
            return True
        except:
            return False

    @staticmethod
    def get_role_by_label(label: str) -> User:
        """Получить роль по label."""
        return Role.query.filter_by(label=label).first()

    def create_role(self, label: str):
        """Создать роль."""
        role = Role(label=label)
        self.db_connection.session.add(role)
        self.db_connection.session.commit()

    def change_role_data(self, role, label: str):
        """Поменять название роли."""
        role.label = label
        self.db_connection.session.commit()

    def change_user_role(self, role, user):
        """Поменять права пользователя."""
        user.role = role
        self.db_connection.session.commit()


@lru_cache()
def get_roles_service() -> RolesService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    cache_storage: CacheStorage = get_redis_storage()
    return RolesService(cache_storage)
