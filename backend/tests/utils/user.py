from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from backend.src.core.config import settings
from backend.src.apps.user.crud import create_user, get_user
from src.models import User


def create_user_for_test(db: Session):
    email = settings.EMAIL_TEST_USER
    password = settings.PASSWORD_TEST_USER
    user_test = get_user(email=email, db=db)
    if not user_test:
        obj_in = User(email=email, password=password, is_admin=True, is_active=True)
        user_in = create_user(db=db, obj_in=obj_in)
        return {"email": email, "password": password, "id": user_in.id}
    return {"email": email, "password": password, "id": user_test.id}


def get_test_user_token_cookie(client: TestClient):
    email = settings.EMAIL_TEST_USER
    password = settings.PASSWORD_TEST_USER
    data = {
        "login": f"{email}",
        "password": f"{password}"
    }
    response = client.post('/login', json=data)
    return response.cookies


def get_cookie_test_user(
        client: TestClient,
        db: Session
):
    create_user_for_test(db=db)
    cookie = get_test_user_token_cookie(client)
    return cookie
