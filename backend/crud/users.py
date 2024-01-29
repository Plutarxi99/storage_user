from sqlalchemy.orm import Session

from backend.core.security import get_password_hash
from backend.models import User
from backend.schemas.admin import PrivateCreateUserModel



def get_user_on_id(
        user_id: int,
        db: Session
):
    """
    Получение пользователя из базы данных по id в базе данных
    :param user_id:  id пользователя
    :param db: подключении к базе данных
    :return: пользователя из базы данных
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_user(
        email: str,
        db: Session
):
    """
    Полечение пользваотеля по email из базы данных
    :param email: email пользователя
    :param db: подключение к базе данных
    :return: пользователя из базы данных
    """
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(
        db: Session,
        *,
        obj_in: PrivateCreateUserModel
):
    """
    Создание пользвоателя с хэшированным паролем и возвращение его
    :param db: подключение к базе данных
    :param obj_in: входные данные для создания пользователя
    :return: созданного пользователя
    """
    db_obj = User(
        email=obj_in.email,
        password=get_password_hash(obj_in.password),
        is_admin=obj_in.is_admin,
        is_active=obj_in.is_active
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_users_all(db: Session):
    users = db.query(User).all()
    return users
