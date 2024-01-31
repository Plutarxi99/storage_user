from sqlalchemy.orm import Session

from backend.src.exceptions.model import ErrorResponseModel
from backend.src.apps.auth.openapi_responses import responses_login
from backend.src.apps.auth.schemas import LoginModel

from backend.src.apps.user.schemas import CurrentUserResponseModel
from backend.src.operations.deps import authenticate_user, get_db
from fastapi import APIRouter, Depends, Response
from datetime import timedelta

from backend.src.core.config import settings
from backend.src.core.security import create_access_token

# собираем эндпоинты для объеденения
router_auth = APIRouter()


@router_auth.post(
    "/login",
    summary="Вход в систему",
    response_model=CurrentUserResponseModel,
    response_model_exclude_none=True,
    responses={**responses_login}
)
async def login_user(
        response: Response,
        user: LoginModel,
        db: Session = Depends(get_db),
):
    """
    Эндпоинт для входа существующего пользователя
    :param response: для установки токена для использования сервиса
    :param user: схема для входa пользователя
    :param db: получение подключения к сессии базе данных
    :return: возвращает существующего пользователя
    """
    # для получения существующего пользователя
    user_in = authenticate_user(email=user.login, password=user.password, db=db)
    # проверка есть ли пользователь
    if not user_in:
        raise ErrorResponseModel(code=401, message="Такого пользователя не существует в системе")
    # установка времени протухания токена, создание и присваивания токена
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    response.set_cookie(key="bearer", value=f"{access_token}")
    return user_in


@router_auth.get(
    "/logout",
    summary="Выход из системы"
)
async def logout_user(
        response: Response
):
    """
    Эндпоинт для удаления bearer token из cookie в браузере пользователя
    :param response: для удаления bearer token из cookie в браузере пользователя
    :return:
    """
    # удаление токена
    response.delete_cookie(key=settings.COOKIE_NAME)
    return {"Выход": "Вы уже вышли из системы"}
