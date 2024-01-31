from datetime import date

from pydantic import BaseModel, EmailStr

from backend.src.operations.validators import PhoneNumberUser


# схемы для ответов и получения данных

class BasePrivate(BaseModel):
    first_name: str | None = "Луций"
    last_name: str | None = "Местрий"
    other_name: str | None = "Плутарх"
    email: EmailStr
    phone: PhoneNumberUser | None = "+79123456789"
    birthday: date | None = "2007-11-07"
    city: str | None = None
    additional_info: str | None = None
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True


class PrivateDetailUserResponseModel(BasePrivate):
    id: int

    class Config:
        orm_mode = True


class PrivateCreateUserModel(BasePrivate):
    password: str

    class Config:
        orm_mode = True


class PrivateUpdateUserModel(PrivateDetailUserResponseModel):
    class Config:
        orm_mode = True
