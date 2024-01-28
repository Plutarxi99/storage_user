import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = os.getenv("COOKIE_NAME")

    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")

    EMAIL_TEST_USER: str = os.getenv("EMAIL_TEST_USER")
    PASSWORD_TEST_USER: str = os.getenv("PASSWORD_TEST_USER")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"


settings = Settings()
