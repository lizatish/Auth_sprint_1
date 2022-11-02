from flask import Blueprint, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate

from api.v1.schemas import RefreshAccessTokensResponse, UserData, PasswordChange, UserRegistration
from api.v1.schemas import UserLoginScheme, AccountHistory
from core.jwt import get_jwt_instance
from services.auth import AuthService, get_auth_service
from services.json import JsonService

api_v1 = Blueprint('api_v1', __name__)
jwt = get_jwt_instance()


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
    get_auth_service().add_to_history(user)

    return JsonService.return_success_response(access_token=access_token, refresh_token=refresh_token)


@api_v1.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> RefreshAccessTokensResponse:
    """Обновляет refresh, access токены по валидному refresh-токену."""
    identity = get_jwt_identity()

    user = AuthService.get_user_by_username(identity['username'])
    if not user:
        return JsonService.return_user_not_found()

    refresh_token = JsonService.get_authorization_header_token(request)
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


@api_v1.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Разлогинивает пользователя."""
    identity = get_jwt_identity()

    user = AuthService.get_user_by_username(identity['username'])
    if not user:
        return JsonService.return_user_not_found()

    access_token = get_jwt()["jti"]
    get_auth_service().logout_user(user.id, access_token)

    return JsonService.return_success_response(msg="User has been logged out")


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """Проверка access-токена, что он не лежит уже в revoked-токенах."""
    jti_access_token = jwt_payload["jti"]

    user = AuthService.get_user_by_username(jwt_payload['sub']['username'])
    if not user:
        return JsonService.return_user_not_found()

    compare_access_tokens = get_auth_service().check_access_token_is_revoked(user.id, jti_access_token)
    return not compare_access_tokens


@api_v1.route("/account-history", methods=["GET"])
@jwt_required()
def account_history():
    """Выводит историю входов аккаунта."""
    identity = get_jwt_identity()

    user = AuthService.get_user_by_username(identity['username'])
    if not user:
        return JsonService.return_user_not_found()

    account_history_data = get_auth_service().get_account_history(user)

    return JsonService.prepare_output(AccountHistory, account_history_data)
