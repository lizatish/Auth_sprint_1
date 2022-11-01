from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate

from api.v1.schemas import RefreshAccessTokensResponse, UserData, PasswordChange, UserRegistration
from api.v1.schemas import UserLoginScheme
from services.auth import AuthService, get_auth_service
from services.json import JsonService

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route("/login", methods=["POST"])
@validate()
def login(body: UserLoginScheme) -> RefreshAccessTokensResponse:
    """Позволяет пользователю войти в систему."""
    user = AuthService.get_user_by_username(body.username)
    if not user:
        return JsonService.return_user_not_found()

    if not user.check_password(body.password):
        return JsonService.return_password_verification_failed()

    access_token, refresh_token = get_auth_service().create_tokens(user)

    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)


@api_v1.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> RefreshAccessTokensResponse:
    """Обновляет refresh, access токены по валидному refresh-токену."""
    identity = get_jwt_identity()

    user = AuthService.get_user_by_username(identity['username'])
    if not user:
        return JsonService.return_user_not_found()

    refresh_token = JsonService.get_refresh_token(request)
    compare_refresh_tokens = get_auth_service().check_refresh_token(user.id, refresh_token)
    if not compare_refresh_tokens:
        return JsonService.return_invalid_refresh_token()

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
