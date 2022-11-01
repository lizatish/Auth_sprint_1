from functools import lru_cache

from flask_jwt_extended import create_access_token, create_refresh_token

from db.cache import CacheStorage
from db.redis import get_redis_storage
from models.db_models import User, Role, db
from models.general import RoleType
from services.cache import CacheService
from services.utils import get_or_create


class AuthService:
    """Сервис авторизации и аутентификации."""

    def __init__(self, cache_storage: CacheStorage):
        """Инициализация сервиса."""
        self.cache_service = CacheService(cache_storage)
        self.db_connection = db

    def update_refresh_token(self, user_id: str, refresh_token: str):
        """Обновить refresh-токен."""
        self.cache_service.set_refresh_token(user_id, refresh_token)

    def create_tokens(self, user: User):
        """Создать access и refresh токены для пользователя."""
        token_user_data = {"username": user.username, "role": user.role.label}
        access_token = create_access_token(identity=token_user_data)
        refresh_token = create_refresh_token(identity=token_user_data)

        self.update_refresh_token(user_id=user.id, refresh_token=refresh_token)

        return access_token, refresh_token

    def update_revoked_access_token(self, user_id: str, revoked_access_token: str):
        """Обновить access-токен."""
        self.cache_service.set_revoked_access_token(user_id, revoked_access_token)

    def create_user(self, username: str, password: str):
        """Создать пользователя."""
        role = get_or_create(self.db_connection.session, Role, label=RoleType.STANDARD)
        user = User(username=username, role=role)
        user.set_password(password)
        self.db_connection.session.add(user)
        self.db_connection.session.commit()

    def change_password(self, user, password: str):
        """Поменять пароль."""
        user.set_password(password)
        self.db_connection.session.commit()

    def change_user_data(self, user, body):
        """Поменять данные пользователя."""
        if (body.username) and (body.username != user.username):
            if not self.get_user_by_username(body.username):
                user.username = body.username
            else:
                return False
        self.db_connection.session.commit()
        return True

    @staticmethod
    def get_user_by_username(username: str) -> User:
        """Получить пользователя по его username."""
        return User.query.filter_by(username=username).first()


@lru_cache()
def get_auth_service() -> AuthService:
    """Возвращает экземпляр сервиса для работы с кинопроизведениями."""
    cache_storage: CacheStorage = get_redis_storage()
    return AuthService(cache_storage)
