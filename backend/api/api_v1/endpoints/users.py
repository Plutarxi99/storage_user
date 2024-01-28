from typing import Annotated
from sqlalchemy.orm import Session
from backend.crud.base import CRUDBase
from backend.crud.users import get_user, get_users_all
from backend.models import User
from backend.pagination.page_users import UserAPIPage
from backend.schemas.auth import LoginModel
from backend.schemas.user import UserSchema, CurrentUserResponseModel, UpdateUserModel, UpdateUserResponseModel, \
    UsersListElementModel
from backend.api.deps import get_db, get_current_user, get_current_active_user
from fastapi import APIRouter, Depends, Body
from fastapi_pagination import paginate

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get(
    "/current",
    summary='Получение данных о текущем пользователе',
    response_model=CurrentUserResponseModel
)
async def get_data_current_user(
        current_user: Annotated[LoginModel, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    """
    Здесь находится вся информация, доступная пользователю о самом себе, а так же информация является ли он администратором
    :return:
    """
    user = get_user(db=db, email=current_user.email)
    return user


@router.patch(
    "/current",
    summary='Изменение данных пользователя',
    response_model=UpdateUserResponseModel
)
async def change_data_current_user(
        update_user_data: Annotated[UpdateUserModel, Body()],
        current_user: Annotated[LoginModel, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    """
    Здесь пользователь имеет возможность изменить свои данные
    :return:
    """
    user = CRUDBase(model=User)
    user.update(db=db, obj_in=update_user_data, db_obj=current_user)
    user_u = get_user(db=db, email=current_user.email)
    return user_u


@router.get(
    "/",
    summary='Постраничное получение кратких данных обо всех пользователях',
    response_model=UserAPIPage[UsersListElementModel]
)
async def get_data_list_user(
        current_user: Annotated[LoginModel, Depends(get_current_user)],
        db: Session = Depends(get_db),
):
    """
    Здесь находится вся информация, доступная пользователю о других пользователях
    :return:
    """
    users = get_users_all(db=db)
    return paginate(users)
