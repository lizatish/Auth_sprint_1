import pytest

from ..settings import get_settings
from ..testdata.users_change_password import (test_data_for_change_password_successfull,
                                              test_data_for_change_password_fail)

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
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}
    db_cursor.execute(f"SELECT * FROM public.user WHERE username='{username['username']}';")
    db_user_before_changing = db_cursor.fetchone()

    response = auth_api_client.post(f'/password-change', json=request_body, headers=headers)
    response_body = response.json
    db_cursor.execute(f"SELECT * FROM public.user WHERE username='{username['username']}';")
    db_user_after_changing = db_cursor.fetchone()

    assert db_user_before_changing['password'] != db_user_after_changing['username']
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body



@pytest.mark.parametrize(
    'username, request_body, expected_body, expected_answer', test_data_for_change_password_fail
)
async def test_change_password_fail(
        auth_api_client, generate_access_token_for_user,
        request_body: dict, expected_body: dict, expected_answer: dict, username: dict
):
    """
    Тест для проверки ошибки смены пароля.

    Проверяет:
    - неудачный ответ от серивиса
    """
    token = generate_access_token_for_user[username['username']]
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    response = auth_api_client.post(f'/password-change', json=request_body, headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
