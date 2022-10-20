from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/')
def hello_world():
    return 'Hello, World!'
