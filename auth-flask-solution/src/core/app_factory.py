from flasgger import Swagger
from flask import Flask

from core.jwt import create_jwt
from db.db_factory import create_db


def create_app(config_filename: object) -> Flask:
    """Фабрика создания приложения."""
    app = Flask(__name__)

    app.config.from_object(config_filename)

    # Инициализация БД
    create_db(app)

    create_jwt(app)
    Swagger(app)

    # Регистрация отдельных компонентов (API)
    from api.v1.auth import auth_v1
    from api.v1.roles import roles_v1

    app.register_blueprint(auth_v1)
    app.register_blueprint(roles_v1)

    return app
