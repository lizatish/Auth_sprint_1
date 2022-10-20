from flask import Flask

from api.v1.routes import api_v1

app = Flask(__name__)

app.register_blueprint(api_v1)

if __name__ == '__main__':
    app.run()
