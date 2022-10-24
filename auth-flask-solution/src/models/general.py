import enum
import re
import uuid

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr

from db.db_factory import get_db

db = get_db()


class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__.lower()).lower()


class UUIDMixin(BaseMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class RoleType(enum.Enum):
    STANDARD = 'standard'
    PRIVILEGED = 'privileged'


class User(UUIDMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(Enum(RoleType))
