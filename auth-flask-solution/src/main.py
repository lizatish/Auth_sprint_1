from flask import Flask
from werkzeug.utils import import_string

from api.v1.routes import api_v1

app = Flask(__name__)

app.register_blueprint(api_v1)
cfg = import_string('core.settings.DevSettings')()
app.config.from_object(cfg)

if __name__ == '__main__':
    app.run()
