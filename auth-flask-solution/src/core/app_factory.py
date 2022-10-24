from flask import Flask
from werkzeug.utils import import_string


def create_app(config_filename: str) -> Flask:
    app = Flask(__name__)

    cfg = import_string(config_filename)()
    app.config.from_object(cfg)

    return app
