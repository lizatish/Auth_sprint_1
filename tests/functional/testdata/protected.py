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
