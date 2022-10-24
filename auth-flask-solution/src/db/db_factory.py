from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy | None = None


def create_db(app):
    global db
    if not db:
        db = SQLAlchemy()
        db.init_app(app)
        with app.app_context():
            from models import general
            db.create_all()
    return db


def get_db():
    return db
