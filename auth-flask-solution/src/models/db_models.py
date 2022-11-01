import re
import uuid

from flask import current_app
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from db.db_factory import get_db


db = get_db()


class BaseMixin:
    """Миксин с базовыми методами для всех моделей."""

    @declared_attr
    def __tablename__(cls):
        """Подставляет snake_case как имя таблицы."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__.lower()).lower()


class UUIDMixin(BaseMixin):
    """Миксин с идентификатором моделей."""

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Role(UUIDMixin, db.Model):
    """Модель пользователя."""

    label = db.Column(db.String, nullable=False)
    users = db.relationship('User', backref='role')


class User(UUIDMixin, db.Model):
    """Модель пользователя."""

    username = db.Column(db.String, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"))
    password = db.Column(db.String(400), nullable=False)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        self.password = generate_password_hash(
            password,
            method=current_app.config['AUTH_HASH_METHOD'],
            salt_length=current_app.config['AUTH_HASH_SALT_LENGTH'],
        )
