import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from tests.functional.settings import get_settings
from tests.functional.testdata.protected import test_data_protected_access

conf = get_settings()
pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'request_body, expected_answer, expected_body', test_data_protected_access
)
def test_protected_access(
        auth_api_client: FlaskClient,
        sqlalchemy_postgres: SQLAlchemy,
        generate_access_token_for_user: dict,
        sync_redis_pool: Redis,
        request_body: dict,
        expected_answer: dict,
        expected_body: dict
):
    access_token = generate_access_token_for_user[request_body['username']]
    headers = {'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'}

    response = auth_api_client.get('/protected', headers=headers)
    response_body = response.json

    assert response.status_code == expected_answer['status']
    assert response_body == expected_body
