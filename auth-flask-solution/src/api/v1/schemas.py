from pydantic import BaseModel, Field
from typing import Optional


class UserLoginScheme(BaseModel):
    username: str
    password: str


class UserRegistration(BaseModel):
    """Схема регистрации."""

    username: str
    password: str = Field(
        regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description="Минимум восемь символов, минимум одна буква и одна цифра"
    )


class PasswordChange(BaseModel):
    """Схема жанра."""

    old_password: str
    new_password: str = Field(
        regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description="Минимум восемь символов, минимум одна буква и одна цифра"
    )


class UserData(BaseModel):
    username: Optional[str]
