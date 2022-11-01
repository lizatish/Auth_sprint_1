from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemas import UserLoginScheme, UserRegistration, PasswordChange, UserData
from services.auth import AuthService, get_auth_service
from services.json import JsonService
from flask_jwt_extended import jwt_required, get_jwt_identity

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route("/login", methods=["POST"])
@validate()
def login(body: UserLoginScheme):
    user = AuthService.get_user_by_username(body.username)
    if not user:
        return JsonService.return_user_not_found()

    if not user.check_password(body.password):
        return JsonService.return_password_verification_failed()

    access_token, refresh_token = get_auth_service().create_tokens(user)

    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)


@api_v1.route("/registration", methods=["POST"])
@validate()
def registration(body: UserRegistration):
    user = AuthService.get_user_by_username(body.username)
    if user:
        return JsonService.return_user_exists()
    get_auth_service().create_user(body.username, body.password)
    return JsonService.return_success_response(msg='Successful registration')


@api_v1.route("/password-change", methods=["POST"])
@validate()
@jwt_required()
def password_change(body: PasswordChange):
    identity = get_jwt_identity()
    user = AuthService.get_user_by_username(identity["username"])
    if not user:
        return JsonService.return_user_not_found()
    if not user.check_password(body.old_password):
        return JsonService.return_password_verification_failed()
    get_auth_service().change_password(user, body.new_password)
    return JsonService.return_success_response(msg='Successful password change')


@api_v1.route("/user", methods=["PUT"])
@validate()
@jwt_required()
def change_user_data(body: UserData):
    identity = get_jwt_identity()
    user = AuthService.get_user_by_username(identity["username"])
    if not user:
        return JsonService.return_user_not_found()
    created = get_auth_service().change_user_data(user, body)
    if not created:
        return JsonService.return_user_exists()
    return JsonService.return_success_response(msg='Successful user data changed')
