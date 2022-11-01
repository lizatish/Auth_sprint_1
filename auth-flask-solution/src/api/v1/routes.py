from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemas import UserLoginScheme
from services.auth import AuthService, get_auth_service
from services.json import JsonService

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
