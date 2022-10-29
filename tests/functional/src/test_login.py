import pytest
from psycopg2._psycopg import cursor

from tests.functional.settings import get_settings
from tests.functional.testdata.login import test_data_for_success_login_user

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_body, expected_answer', test_data_for_success_login_user
)
async def test_success_login_user(
        auth_api_client,
        db_cursor: cursor,
        request_body: dict,
        expected_body: dict,
        expected_answer: dict,
):
    response = auth_api_client.post(f'/login', json=request_body)
    response_body = response.json
    db_cursor.execute(f"SELECT * FROM public.user WHERE username='{request_body['username']}';")
    db_user = db_cursor.fetchone()

    assert db_user['username'] == request_body['username']
    assert response.status_code == expected_answer['status']
    assert response_body == expected_body


def test_not_exists_login_user():
    pass


def test_not_correct_password_login_user():
    pass
