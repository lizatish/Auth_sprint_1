from flask import Blueprint, request
import orjson
from typing import Optional
from models.db_models import User
from .schemas import UserRegistration, UserInfo, PasswordChande, UserLoginScheme, UserData, Role, RoleRepresentation, RoleManagerQuery
from flask_pydantic import validate
from services.json import JsonService
from services.auth import AuthService, get_auth_service
from services.roles import RolesService, get_roles_service
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from core.settings import get_settings

conf = get_settings()
api_v1 = Blueprint('api_v1', __name__)



@api_v1.route('/scope', methods=["GET"])
def users_scope():
    users = User.query.all()
    return [orjson.loads(UserInfo(
        id=item.id,
        username=item.username,
        role=item.role.label,
    ).json()) for item in users]


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
def password_change(body: PasswordChande):
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


@api_v1.route("/role", methods=["POST"])
@validate()
def roles_create(body: Role):
    role = RolesService.get_role_by_label(body.label)
    if role:
        return JsonService.return_role_exists()
    get_roles_service().create_role(body.label)
    return JsonService.return_success_response(msg="Role created!")


@api_v1.route("/role", methods=["GET"])
def roles_scope():
    roles = RolesService.get_roles()
    return [orjson.loads(RoleRepresentation(
        id=item.id,
        label=item.label
    ).json()) for item in roles]



@api_v1.route("/role/<role_id>", methods=["GET"])
def role_retriew(role_id):
    role = RolesService.get_role_by_id(role_id)
    if not role:
        return JsonService.return_role_not_found()
    return orjson.loads(RoleRepresentation(
        id=role.id,
        label=role.label
    ).json())


@api_v1.route("/role/<role_id>", methods=["DELETE"])
def role_delete(role_id):
    deleted = get_roles_service().delete_role_by_id(role_id)
    if deleted:
        return JsonService.return_success_response(msg="Role deleted!")
    return JsonService.return_role_not_found()


@api_v1.route("/role/<role_id>", methods=["PUT"])
@validate()
def role_update(role_id, body: Role):
    role = RolesService.get_role_by_id(role_id)
    if not role:
        return JsonService.return_role_not_found()
    get_roles_service().change_role_data(role, body.label)
    return JsonService.return_success_response(msg='Successful role data changed')


@api_v1.route("/role-manager/<user_id>", methods=["GET"])
@validate()
def role_appoint(user_id, query: RoleManagerQuery):
    role = RolesService.get_role_by_id(query.role_id) #request.args.get('role_id')
    if not role:
        return JsonService.return_role_not_found()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role(role, user)
    return JsonService.return_success_response(msg="Role changed!")


@api_v1.route("/role-manager/<user_id>", methods=["DELETE"])
def role_take_away(user_id):
    role = RolesService.get_role_by_label(conf.DEFAULT_ROLE_NAME)
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role(role, user)
    return JsonService.return_success_response(msg="Role changed!")


@api_v1.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return JsonService.return_success_response(msg=identity['role'])
