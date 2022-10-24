from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy | None = None


def create_db(app: Flask):
    """Инициализирует бд для алхимии."""
    global db
    db = SQLAlchemy()
    db.init_app(app)
    with app.app_context():
        from models import db_models  # noqa
        db.create_all()


def get_db() -> SQLAlchemy:
    """Возвращает экземпляр алхимии."""
    return db
