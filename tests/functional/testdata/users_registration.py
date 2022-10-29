from http import HTTPStatus

test_data_for_registration_successfull = [
    (
        {
            "username": "test27",
            "password": "test8Anadssf"
        },
        {'msg': 'Successful registration'},
        {'status': HTTPStatus.OK},
    ),
    (
        {
            "username": "test",
            "password": "qwe1Er23"
        },
        {'msg': 'Successful registration'},
        {'status': HTTPStatus.OK},
    ),
]

test_data_for_registration_user_exists = [
    (
        {
            "username": "test28",
            "password": "test8Anadssf"
        },
        {
            "msg": "User with this username already exists!"
        },
        {'status': HTTPStatus.CONFLICT},
    ),
    (
        {
            "username": "test29",
            "password": "test8Anadssf"
        },
        {
            "msg": "User with this username already exists!"
        },
        {'status': HTTPStatus.CONFLICT},
    ),
]

test_data_for_registration_bad_password = [
    (
        {
            "username": "test29",
            "password": "test"
        },
        {
            "validation_error": {
                "body_params": [
                    {
                        "ctx": {
                            "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
                        },
                        "loc": [
                            "password"
                        ],
                        "msg": "string does not match regex \"^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$\"",
                        "type": "value_error.str.regex"
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
    (
        {
            "username": "test29",
            "password": "qwertyuio"
        },
        {
            "validation_error": {
                "body_params": [
                    {
                        "ctx": {
                            "pattern": "^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$"
                        },
                        "loc": [
                            "password"
                        ],
                        "msg": "string does not match regex \"^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$\"",
                        "type": "value_error.str.regex"
                    }
                ]
            }
        },
        {'status': HTTPStatus.BAD_REQUEST},
    ),
]