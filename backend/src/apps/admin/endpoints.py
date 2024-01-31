from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_pagination import paginate
from sqlalchemy.orm import Session
from starlette import status

from backend.src.operations.deps import get_db, get_current_admin_user
from backend.src.base.crud import CRUDBase
from backend.src.apps.user.crud import get_user, create_user, get_user_on_id, get_users_all
from backend.src.exceptions.model import ErrorResponseModel
from backend.src.models import User
from backend.src.apps.admin.pagination import AdminAPIPage
from backend.src.apps.admin.openapi_responses import base_response_admin
from backend.src.exceptions.openapi_responses import responses_not_found_404
from backend.src.apps.admin.schemas import PrivateDetailUserResponseModel, PrivateCreateUserModel, PrivateUpdateUserModel
from backend.src.apps.user.schemas import UsersListElementModel

router_admin = APIRouter(
    dependencies=[
        Depends(get_current_admin_user)
    ],
    responses={
        **base_response_admin
    }
)


@router_admin.get(
    "/users",
    summary="Постраничное получение кратких данных обо всех пользователях",
    response_model=AdminAPIPage[UsersListElementModel],
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


@router_admin.post(
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


@router_admin.get(
    "/users/{pk}",
    summary="Детальное получение информации о пользователе",
    response_model=PrivateDetailUserResponseModel,
    responses={
        **responses_not_found_404
    }
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


@router_admin.delete(
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


@router_admin.patch(
    "/users/{pk}",
    summary="Изменение информации о пользователе",
    response_model=PrivateUpdateUserModel,
    responses={
        **responses_not_found_404
    }
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
    email_in_bd = user_for_update.email
    email_for_update = update_user_data.email
    if email_in_bd == email_for_update:
        raise ErrorResponseModel(code=400, message="Такой email уже есть в базе данных")
    user = CRUDBase(model=User)
    user.update(db=db, obj_in=update_user_data, db_obj=user_for_update)
    user_u = get_user_on_id(db=db, user_id=pk)
    return user_u
