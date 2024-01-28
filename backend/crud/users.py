from typing import Annotated, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.core.security import get_password_hash
from backend.models import User
from backend.schemas.admin import PrivateCreateUserModel
from backend.schemas.user import UserSchema, UpdateUserModel


def get_user_on_id(
        user_id: int,
        db: Session
):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_user(
        email: str,
        db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(db: Session, *, obj_in: PrivateCreateUserModel):
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
