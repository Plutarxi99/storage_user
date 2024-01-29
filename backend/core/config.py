import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')


# Настройки для приложения
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # секретный ключ для сервиса
    ALGORITHM: str = "HS256"  # алгоритм для создания хэшированного пароля
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # время протухания токена
    COOKIE_NAME: str = os.getenv("COOKIE_NAME")  # названия присваемого токена в cookie

    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL")  # email суперпользователя или первого в бд
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")  # пароль суперпользователя или первого в бд

    EMAIL_TEST_USER: str = os.getenv("EMAIL_TEST_USER")  # email тестового пользователя
    PASSWORD_TEST_USER: str = os.getenv("PASSWORD_TEST_USER")  # пароль тестового пользователя

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    # ссылка для подключения к базe данных
    SQLALCHEMY_DATABASE_URI: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"


settings = Settings()
