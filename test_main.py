import pytest
from flask import testing
import main
from http import HTTPStatus


@pytest.fixture
def test_client() -> testing.FlaskClient:
    return main.App.test_client()


def test_frontend_route(test_client: testing.FlaskClient) -> None:
    retval = test_client.get('/')
    assert retval.status_code == HTTPStatus.OK
    assert b'Yahoo' in retval.data
