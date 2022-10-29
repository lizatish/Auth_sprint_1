def test_get_film_by_id_successful(auth_api_client):
    response = auth_api_client.get("/scope")
    assert response.status_code == 200


import pytest

from ..settings import get_settings
from ..testdata.users import (test_data_for_registration_successfull,
                              test_data_for_registration_user_exists,
                              test_data_for_registration_bad_password)

from psycopg2.extensions import connection as _connection


conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_registration_successfull
)
async def test_regustration_successfull(
        auth_api_client, db_cursor,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки успешных запросов на регистрацию.

    Проверяет:
    - наличие пользователя после регистрации в бд
    - успешный ответ от серивиса
    """
    response = auth_api_client.post(f'/registration', json=request_body)
    response_body = response.json
    db_cursor.execute(f"SELECT * FROM public.user WHERE username='{request_body['username']}';")
    db_user = db_cursor.fetchone()

    assert db_user['username'] == request_body['username']
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_registration_user_exists
)
async def test_regustration_user_exists(
        auth_api_client,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки ошибки регистрации при существовании пользователя с таким логином.

    Проверяет:
    - неудачный ответ от серивиса
    """
    auth_api_client.post(f'/registration', json=request_body)

    response = auth_api_client.post(f'/registration', json=request_body)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_registration_bad_password
)
async def test_regustration_bad_password(
        auth_api_client,
        request_body: dict, expected_body: dict, expected_answer: dict
):
    """
    Тест для проверки ошибки регистрации при существовании пользователя с таким логином.

    Проверяет:
    - неудачный ответ от серивиса
    """
    response = auth_api_client.post(f'/registration', json=request_body)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
