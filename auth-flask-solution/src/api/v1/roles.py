from flask import Blueprint
from flask_pydantic import validate

from api.v1.schemas import Role, RoleRepresentation
from services.auth import AuthService
from services.roles import RolesService, get_roles_service
from services.json import JsonService
from services.utils import is_valid_uuid


roles_v1 = Blueprint('roles_v1', __name__)


@roles_v1.route("/role", methods=["POST"])
@validate()
def roles_create(body: Role):
    role = RolesService.get_role_by_label(body.label)
    if role:
        return JsonService.return_role_exists()
    get_roles_service().create_role(body.label)
    return JsonService.return_success_response(msg="Role created!")


@roles_v1.route("/role", methods=["GET"])
def roles_scope():
    roles = RolesService.get_roles()
    return JsonService.prepare_output(RoleRepresentation, roles)


@roles_v1.route("/role/<role_id>", methods=["GET"])
def role_retriew(role_id):
    if not is_valid_uuid(role_id):
        return JsonService.return_uuid_fail()
    role = RolesService.get_role_by_id(role_id)
    if not role:
        return JsonService.return_role_not_found()
    return JsonService.prepare_single_output(RoleRepresentation, role)


@roles_v1.route("/role/<role_id>", methods=["DELETE"])
def role_delete(role_id):
    if not is_valid_uuid(role_id):
        return JsonService.return_uuid_fail()
    deleted = get_roles_service().delete_role_by_id(role_id)
    if deleted:
        return JsonService.return_success_response(msg="Role deleted!")
    return JsonService.return_role_not_found()


@roles_v1.route("/role-manager/<user_id>", methods=["GET"])
@validate()
def role_appoint(user_id, query: Role):
    if not is_valid_uuid(user_id):
        return JsonService.return_uuid_fail()
    role = RolesService.get_role_by_label(query.label)
    if not role:
        return JsonService.return_role_not_found()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role(role, user)
    return JsonService.return_success_response(msg="Role changed!")


@roles_v1.route("/role-manager/<user_id>", methods=["DELETE"])
def role_take_away(user_id):
    if not is_valid_uuid(user_id):
        return JsonService.return_uuid_fail()
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return JsonService.return_user_not_found()
    get_roles_service().change_user_role_to_default(user)
    return JsonService.return_success_response(msg="Role changed!")
