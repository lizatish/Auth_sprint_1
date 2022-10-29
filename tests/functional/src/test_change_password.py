import pytest

from ..settings import get_settings
from ..testdata.users_change_password import (test_data_for_change_password_successfull)

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'username, request_body, expected_body, expected_answer', test_data_for_change_password_successfull
)
async def test_change_password_successfull(
        auth_api_client, db_cursor, generate_access_token_for_user,
        request_body: dict, expected_body: dict, expected_answer: dict, username: dict
):
    """
    Тест для проверки успешных запросов на смену пароля.

    Проверяет:
    - что пароль в бд поменялся
    - успешный ответ от серивиса
    """
    token = generate_access_token_for_user[username['username']]
    print(token)
    # db_cursor.execute(f"SELECT * FROM public.user WHERE username='{request_body['username']}';")
    # db_user_before_changing = db_cursor.fetchone()
    # response = auth_api_client.post(f'/password-change', json=request_body)
    # response_body = response.json
    # db_cursor.execute(f"SELECT * FROM public.user WHERE username='{request_body['username']}';")
    # db_user_after_changing = db_cursor.fetchone()

    # assert db_user_before_changing['password'] != db_user_after_changing['username']
    # assert response.status_code == expected_answer['status']
    # assert response_body == expected_body
    assert 1 == 2


# @pytest.mark.parametrize(
#     'request_body, expected_body, expected_answer', test_data_for_registration_user_exists
# )
# async def test_registration_user_exists(
#         auth_api_client,
#         request_body: dict, expected_body: dict, expected_answer: dict
# ):
#     """
#     Тест для проверки ошибки регистрации при существовании пользователя с таким логином.

#     Проверяет:
#     - неудачный ответ от серивиса
#     """
#     auth_api_client.post(f'/registration', json=request_body)

#     response = auth_api_client.post(f'/registration', json=request_body)
#     response_body = response.json

#     assert response.status_code == expected_answer['status']
#     assert response_body == expected_body


# @pytest.mark.parametrize(
#     'request_body, expected_body, expected_answer', test_data_for_registration_bad_password
# )
# async def test_registration_bad_password(
#         auth_api_client,
#         request_body: dict, expected_body: dict, expected_answer: dict
# ):
#     """
#     Тест для проверки ошибки регистрации при существовании пользователя с таким логином.

#     Проверяет:
#     - неудачный ответ от серивиса
#     """
#     response = auth_api_client.post(f'/registration', json=request_body)
#     response_body = response.json

#     assert response.status_code == expected_answer['status']
#     assert response_body == expected_body
