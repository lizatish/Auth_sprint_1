from http import HTTPStatus

from models.general import RoleType

test_data_protected_access = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'STANDARD'}
    ),
    (
        {
            'username': 'admin',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.OK},
        {'msg': 'ADMIN'}
    )
]

test_data_test_protected_admin_access_only_success = [
    (
        {
            'username': 'admin',
            'role': RoleType.ADMIN.name
        },
        {'status': HTTPStatus.OK},
    )
]
test_data_test_protected_admin_access_only_success_failed = [
    (
        {
            'username': 'ivan',
            'role': RoleType.STANDARD.name
        },
        {'status': HTTPStatus.FORBIDDEN},
        {"msg": "Admins only!"}
    ),
]
