import re
import uuid

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from db.db_factory import get_db
from models.general import RoleType

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


class User(UUIDMixin, db.Model):
    """Модель пользователя."""

    username = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(Enum(RoleType))
    password = db.Column(db.String(400), nullable=False)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        self.password = generate_password_hash(password, method=f'pbkdf2:sha256:8000', salt_length=16)
