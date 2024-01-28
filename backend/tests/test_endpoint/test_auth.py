from typing import Dict

from starlette import status
from starlette.testclient import TestClient

from backend.core.config import settings


def test_login_user(
        client: TestClient, create_user_test
):
    data = {
        "login": create_user_test["email"],
        "password": create_user_test["password"]
    }
    response = client.post('/login', json=data)
    assert response.status_code == status.HTTP_200_OK


def test_fail_login_user(
        client: TestClient
):
    data = {
        "login": "noregister@test.test",
        "password": "test"
    }
    response = client.post('/login', json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == 'Такого пользователя не существует'


def test_logout_user(client):
    cookie_on = {"bearer": "bearer_token"}
    response_logout = client.get('/logout', cookies=cookie_on)
    assert response_logout.status_code == status.HTTP_200_OK
    assert response_logout.json() == {"Выход": "Вы уже вышли из системы"}
