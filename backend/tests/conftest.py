import pytest
from fastapi.testclient import TestClient

# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from backend.api.deps import get_db
from backend.db.session import Base
from .utils.user import get_test_user_token_cookie, get_cookie_test_user, create_user_for_test
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db):
    # Dependency override
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def test_user_token_cookie(client: TestClient):
    return get_test_user_token_cookie(client)


@pytest.fixture(scope="module")
def test_user_cookie(client: TestClient, db: Session):
    return get_cookie_test_user(client, db)


@pytest.fixture(scope="module")
def create_user_test(db: Session):
    return create_user_for_test(db)
