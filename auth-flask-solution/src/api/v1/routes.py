from flask import Blueprint

from models.db_models import User

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/')
def hello_world():
    users = User.query.all()

    return users
