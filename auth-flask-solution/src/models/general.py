import enum


class RoleType(enum.Enum):
    """Тип роли пользователя."""

    STANDARD = 'standard'
    PRIVILEGED = 'privileged'
    ADMIN = 'admin'
