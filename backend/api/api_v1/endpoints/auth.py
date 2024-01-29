from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.exceptions import ErrorResponseModel
from backend.schemas.add_responses.auth import responses_login
from backend.schemas.auth import LoginModel
from backend.schemas.error import ErrorResponseSchema

from backend.schemas.user import CurrentUserResponseModel
from backend.api.deps import authenticate_user, get_db
from fastapi import APIRouter, Depends, Response, HTTPException
from datetime import timedelta

from backend.core.config import settings
from backend.core.security import create_access_token

# собираем эндпоинты для объеденения
router = APIRouter()


@router.post(
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
    :param db:
    :return:
    """
    # для получения существующего пользователя
    user_in = authenticate_user(email=user.login, password=user.password, db=db)
    # проверка есть ли пользователь
    if not user_in:
        # ответ если нет пользователя
        return JSONResponse(status_code=400, content={"code": 400, "message": "Не существует такого пользователя"})
    # установка времени протухания токена, создание и присваивания токена
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    response.set_cookie(key="bearer", value=f"{access_token}")
    return user_in


@router.get(
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
    response.delete_cookie(key="bearer")
    return {"Выход": "Вы уже вышли из системы"}
