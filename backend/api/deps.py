from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from backend.core.config import settings
from backend.core.security import verify_password, OAuth2PasswordBearerWithCookie
from backend.crud.users import get_user
from backend.exceptions import ErrorResponseModel
from backend.schemas.token import TokenData
from backend.schemas.user import UserSchema

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = OAuth2PasswordBearerWithCookie()


def get_db(request: Request):
    return request.state.db


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
        current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    if not current_user.is_admin:
        raise ErrorResponseModel(code=403, message="вы не админ")
    return current_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db=db, email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
