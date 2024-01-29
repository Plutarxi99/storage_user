from starlette import status
from starlette.testclient import TestClient


def test_get_data_current_user(
        client: TestClient, test_user_cookie
):
    response = client.get('/users/current', cookies=test_user_cookie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'first_name': None, 'last_name': None, 'other_name': None, 'email': 'test@test.ru',
                               'phone': None, 'birthday': None, 'is_admin': True}


def test_change_data_current_user(
        client: TestClient, test_user_cookie
):
    data = {
        "first_name": "string",
        "last_name": "string",
        "other_name": "string",
        "email": "test@test.ru",
        "phone": "string",
        "birthday": "string"
    }
    response = client.patch('/users/current', json=data, cookies=test_user_cookie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 3, 'first_name': 'string', 'last_name': 'string', 'other_name': 'string',
                               'email': 'test@test.ru', 'phone': 'string', 'birthday': 'string'}


# TODO: Не понятная причина не авторизованного пользователя
def test_get_data_list_user(
        client: TestClient, test_user_token_cookie
):
    data = {
        "page": "1",
        "size": "10"
    }
    response = client.get('/users', cookies=test_user_token_cookie)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
