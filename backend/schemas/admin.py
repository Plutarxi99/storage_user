from pydantic import BaseModel

# схемы для ответов и получения данных
class PrivateDetailUserResponseModel(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None
    city: str | None = None
    additional_info: str | None = None
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True


class PrivateCreateUserModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None
    city: str | None = None
    additional_info: str | None = None
    is_admin: bool
    password: str
    is_active: bool

    class Config:
        orm_mode = True


class PrivateUpdateUserModel(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None
    city: str | None = None
    additional_info: str | None = None
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True
