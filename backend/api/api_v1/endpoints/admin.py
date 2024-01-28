from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response, Body
from fastapi_pagination import paginate
from sqlalchemy.orm import Session
from starlette import status

from backend.api.deps import get_db, get_current_admin_user
from backend.crud.base import CRUDBase
from backend.crud.users import get_user, create_user, get_user_on_id, get_users_all
from backend.models import User
from backend.pagination.page_admin import AdminAPIPage
from backend.schemas.admin import PrivateDetailUserResponseModel, PrivateCreateUserModel, PrivateUpdateUserModel
from backend.schemas.user import UserSchema, UsersListElementModel

router = APIRouter(
    dependencies=[Depends(get_current_admin_user)],
                   )


@router.get(
    "/users",
    summary="Постраничное получение кратких данных обо всех пользователях",
    response_model=AdminAPIPage[UsersListElementModel]
)
async def get_list_data_user(
        db: Session = Depends(get_db),
):
    """
    Здесь находится вся информация, доступная пользователю о других пользователях
    :return:
    """
    users = get_users_all(db=db)
    return paginate(users)



@router.post(
    "/users",
    summary="Создание пользователя",
    response_model=PrivateDetailUserResponseModel,
    status_code=status.HTTP_201_CREATED
)
async def add_user_in_db(
        user: PrivateCreateUserModel,
        db: Session = Depends(get_db)
):
    """
    Здесь возможно занести в базу нового пользователя с минимальной информацией о нем
    :return:
    """
    db_user = get_user(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, obj_in=user)


@router.get(
    "/users/{pk}",
    summary="Детальное получение информации о пользователе",
    response_model=PrivateDetailUserResponseModel
)
async def get_user_from_db(
        pk: int,
        db: Session = Depends(get_db)
):
    """
    Здесь администратор может увидеть всю существующую пользовательскую информацию
    :return:
    """
    user = get_user_on_id(db=db, user_id=pk)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="нет такого пользователя"
        )
    return user


@router.delete(
    "/users/{pk}",
    summary="Удаление пользователя",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        pk: int,
        db: Session = Depends(get_db)
):
    """
    Удаление пользователя
    :return:
    """
    user = CRUDBase(model=User)
    user.remove(db=db, id=pk)
    return status.HTTP_204_NO_CONTENT


@router.patch(
    "/users/{pk}",
    summary="Изменение информации о пользователе",
    response_model=PrivateUpdateUserModel
)
async def change_data_user(
        pk: int,
        update_user_data: Annotated[PrivateUpdateUserModel, Body()],
        db: Session = Depends(get_db)
):
    """
    Здесь администратор может изменить любую информацию о пользователе
    :return:
    """
    user_for_update = get_user_on_id(db=db, user_id=pk)
    user = CRUDBase(model=User)
    user.update(db=db, obj_in=update_user_data, db_obj=user_for_update)
    user_u = get_user_on_id(db=db, user_id=pk)
    return user_u
