import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator


# схемы для ответов и получения данных

class BasePrivate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: EmailStr
    phone: str | None = None
    birthday: str | None = None
    city: str | None = None
    additional_info: str | None = None
    is_admin: bool
    is_active: bool

    @field_validator('phone')
    @classmethod
    def check_phone(cls, v: str) -> str:
        try:
            if v[0] == "+":
                int(v[1:])
            phonenumbers.parse(v, None)
            return v
        except:
            raise ValueError(f'Не правильно набран номер {v}')

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
    pass

    class Config:
        orm_mode = True
