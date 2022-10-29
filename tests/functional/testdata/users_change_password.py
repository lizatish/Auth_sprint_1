from http import HTTPStatus

test_data_for_change_password_successfull = [
    (
        {"username": "oleg"},
        {
            "old_password":"tedsvsd1B",
            "new_password":"tedsvsd1A"
        },
        {'msg': 'Successful password change'},
        {'status': HTTPStatus.OK},
    ),
    (
        {"username": "liza"},
        {
            "old_password":"tedsvsd1B",
            "new_password":"tedsvsd1A"
        },
        {'msg': 'Successful password change'},
        {'status': HTTPStatus.OK},
    ),
]