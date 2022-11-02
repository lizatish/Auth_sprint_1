from functools import wraps

from flask_jwt_extended import (
    get_jwt_identity
)

from models.general import RoleType
from services.json import JsonService


def admin_required(fn):
    """Проверяет доступ только для администратора."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity['role'] != RoleType.ADMIN.name:
            return JsonService().return_admins_only()
        else:
            return fn(*args, **kwargs)

    return wrapper
