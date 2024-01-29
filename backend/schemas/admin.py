from pydantic import BaseModel, EmailStr


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
