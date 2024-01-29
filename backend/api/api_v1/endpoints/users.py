from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.core.config import settings
from backend.core.security import create_access_token
from backend.crud.base import CRUDBase
from backend.crud.users import get_user, get_users_all
from backend.models import User
from backend.pagination.page_users import UserAPIPage
from backend.schemas.add_responses.users import responses_update_current_user, responses_base_users
from backend.schemas.auth import LoginModel
from backend.schemas.user import UserSchema, CurrentUserResponseModel, UpdateUserModel, UpdateUserResponseModel, \
    UsersListElementModel
from backend.api.deps import get_db, get_current_user, get_current_active_user
from fastapi import APIRouter, Depends, Body, Response
from fastapi_pagination import paginate

router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
    responses={**responses_base_users}
)


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
    if not user:
        return JSONResponse(
            status_code=400, content={}
        )
    return user


@router.patch(
    "/current",
    summary='Изменение данных пользователя',
    response_model=UpdateUserResponseModel,
    responses={
        **responses_update_current_user
    }
)
async def change_data_current_user(
        response: Response,
        update_user_data: Annotated[UpdateUserModel, Body()],
        current_user: Annotated[LoginModel, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    """
    Здесь пользователь имеет возможность изменить свои данные
    :return:
    """
    user = CRUDBase(model=User)
    user.update(db=db, obj_in=update_user_data, db_obj=current_user)
    user_u = get_user(db=db, email=current_user.email)
    # при изменение в базе данных email пользователя
    # bearer token не действителен и мы пересохраняем bearer token пользователю
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": update_user_data.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="bearer", value=f"{access_token}")
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
