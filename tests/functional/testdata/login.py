from http import HTTPStatus

test_data_for_success_login_user = [
    (
        {
            "username": "ivan",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.OK},
    ),
    (
        {
            "username": "liza",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_unsuccess_login_user = [
    (
        {
            "username": "ivanovivanov",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
    (
        {
            "username": "lizaliza",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
]

test_data_for_not_exists_login_user = [
    (
        {
            "username": "ivanovivanov",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
    (
        {
            "username": "lizaliza",
            "password": "ivanivanov"
        },
        {'status': HTTPStatus.NOT_FOUND},
    ),
]

test_data_for_not_correct_password_login_user = [
    (
        {
            "username": "ivan",
            "password": "123456"
        },
        {'status': HTTPStatus.UNAUTHORIZED},
    ),
    (
        {
            "username": "liza",
            "password": "lsKFSLkdmskdmfs"
        },
        {'status': HTTPStatus.UNAUTHORIZED},
    ),
]
