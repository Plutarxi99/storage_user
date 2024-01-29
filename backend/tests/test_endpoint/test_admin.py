from starlette import status
from starlette.testclient import TestClient


def test_get_list_data_user(
        client: TestClient, test_user_cookie
):
    data = {
        "page": "1",
        "size": "10"
    }
    response = client.get("/private/users", params=data, cookies=test_user_cookie)
    assert response.status_code == status.HTTP_200_OK


def test_add_user_in_db(
        client: TestClient, test_user_cookie
):
    data = {
        "first_name": "string",
        "last_name": "string",
        "other_name": "string",
        "email": "test_create@test.ru",
        "phone": "+79527777777",
        "birthday": "2020-02-02",
        "city": "string",
        "additional_info": "string",
        "is_admin": True,
        "password": "test",
        "is_active": True
    }
    response = client.post("/private/users", json=data, cookies=test_user_cookie)
    assert response.status_code == status.HTTP_201_CREATED


def test_get_user_from_db(
        client: TestClient, test_user_cookie
):
    pk = 1
    response = client.get(f'/private/users/{pk}', cookies=test_user_cookie)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1


def test_delete_user(
        client: TestClient, test_user_cookie, create_user_test
):
    pk = create_user_test["id"]
    response = client.delete(f'/private/users/{pk}', cookies=test_user_cookie)
    assert response.status_code == status.HTTP_204_NO_CONTENT
