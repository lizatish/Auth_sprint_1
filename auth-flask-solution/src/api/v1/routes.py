from flask import Blueprint
import orjson

from models.db_models import User
from .schemas import UserRegistration, UserInfo, PasswordChande
from flask_pydantic import validate
from services.json import JsonService
from services.auth import AuthService, get_auth_service
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api_v1 = Blueprint('api_v1', __name__)



@api_v1.route('/scope', methods=["GET"])
def users_scope():
    users = User.query.all()
    return [orjson.loads(UserInfo(
        id=item.id,
        username=item.username,
        role=item.role.value,
    ).json()) for item in users]


@api_v1.route("/registration", methods=["POST"])
@validate()
def registration(body: UserRegistration):
    user = AuthService.get_user_by_username(body.username)
    if user:
        return JsonService.return_user_exists()
    get_auth_service().create_user(body.username, body.password)
    return JsonService.return_success_response(message='Successful registration')


# @api_v1.route("/password-change", methods=["POST"])
# @validate()
# @jwt_required()
# def password_change(body: PasswordChande):
#     identity = get_jwt_identity()
#     user = AuthService.get_user_by_username(identity.username)
#     if user:
#         return JsonService.return_user_exists()
#     user.check_password
#     get_auth_service().
#     return JsonService.return_success_response(message='Successful registration')
