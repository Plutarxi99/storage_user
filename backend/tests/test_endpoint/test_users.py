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
        "phone": "+79527777777",
        "birthday": "2022-02-02"
    }
    response = client.patch('/users/current', json=data, cookies=test_user_cookie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'email': 'test@test.ru', 'first_name': 'string', 'last_name': 'string',
                               'other_name': 'string', 'phone': '+79527777777', 'birthday': '2022-02-02', 'id': 3}


def test_get_data_list_user(
        client: TestClient, test_user_token_cookie
):
    response = client.get('/users', cookies=test_user_token_cookie)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
