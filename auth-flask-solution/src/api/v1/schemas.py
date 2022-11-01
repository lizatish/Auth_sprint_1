from pydantic import BaseModel, Field


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
