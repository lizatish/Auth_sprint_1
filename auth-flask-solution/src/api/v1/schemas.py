from uuid import UUID
from pydantic import BaseModel, Field
import orjson


def orjson_dumps(v, *, default):
    """Функция-подмена для быстрой работы c json."""
    return orjson.dumps(v, default=default).decode()


class UserRegistration(BaseModel):
    """Схема жанра."""

    username: str
    password: str = Field(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", description="Минимум восемь символов, минимум одна буква и одна цифра")


class UserInfo(BaseModel):
    """Схема персоны."""

    id: UUID
    username: str
    role: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PasswordChande(BaseModel):
    """Схема жанра."""

    old_password: str
    new_password: str = Field(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", description="Минимум восемь символов, минимум одна буква и одна цифра")
