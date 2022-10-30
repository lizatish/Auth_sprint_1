from http import HTTPStatus

test_data_for_success_login_user = [
    (
        {
            "username": "ivan",
            "password": "ivanivanov"
        },
        ['access_token', 'refresh_token'],
        {'status': HTTPStatus.OK},
    ),
    # (
    #     {
    #         "username": "test",
    #         "password": "qwe1Er23"
    #     },
    #     {'message': 'Successful registration'},
    #     {'status': HTTPStatus.OK},
    # ),
]