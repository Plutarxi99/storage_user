import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from backend.src.core.config import settings
from backend.src.core.security import get_password_hash
from backend.src.database import SessionLocal
from backend.src.models import User
from backend.src.apps.user.crud import get_user


# TODO: создание в новой базе данных первого пользователя для управления ею
def get_db_for_create_superuser():
    db = SessionLocal()
    db.begin()
    # try:
    #     yield db
    # finally:
    #     db.close()
    return db


def create_superuser(db):
    """
    Создание первого пользователя для сервиса
    """
    user = get_user(db=db, email=settings.SUPERUSER_EMAIL)
    if not user:
        db_obj = User(
            email=settings.SUPERUSER_EMAIL,
            password=get_password_hash(settings.SUPERUSER_PASSWORD),
            is_admin=True,
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        db.close()


if __name__ == "__main__":
    create_superuser(db=get_db_for_create_superuser())
    print("Суперпользователь создан")
