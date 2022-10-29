from flask import Flask
from flask_jwt_extended import JWTManager
from db.db_factory import create_db


def create_app(config_filename: object) -> Flask:
    """Фабрика создания приложения."""
    app = Flask(__name__)

    app.config.from_object(config_filename)

    # Инициализация БД
    create_db(app)
    jwt = JWTManager(app)
    # Регистрация отдельных компонентов (API)
    from api.v1.routes import api_v1

    app.register_blueprint(api_v1)

    return app
