from sqlalchemy.orm import Session

from backend.exceptions import ErrorResponseModel
from backend.schemas.auth import LoginModel

from backend.schemas.user import CurrentUserResponseModel
from backend.api.deps import authenticate_user, get_db
from fastapi import APIRouter, Depends, Response
from datetime import timedelta

from backend.core.config import settings
from backend.core.security import create_access_token

router = APIRouter()


@router.post(
    "/login",
    summary="Вход в систему",
    response_model=CurrentUserResponseModel,
    response_model_exclude_none=True
)
async def login_user(
        response: Response,
        user: LoginModel,
        db: Session = Depends(get_db),
):
    user_in = authenticate_user(email=user.login, password=user.password, db=db)
    if not user_in:
        # raise HTTPException(status_code=400, detail="Такого пользователя не существует")
        raise ErrorResponseModel(code=401, message="Такого пользователя не существует")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    response.set_cookie(key="bearer", value=f"{access_token}")
    return user_in


@router.get("/logout", summary="Выход из системы")
async def logout_user(
        response: Response
):
    response.delete_cookie(key="bearer")
    return {"Выход": "Вы уже вышли из системы"}
