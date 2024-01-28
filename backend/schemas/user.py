from typing import List, Dict

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    # email: EmailStr


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    phone: str | None = None
    birthday: str | None = None
    city: str | None = None
    additional_info: str | None = None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
        from_attributes = True


class CurrentUserResponseModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUserModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None

    class Config:
        orm_mode = True


class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    other_name: str | None = None
    email: str
    phone: str | None = None
    birthday: str | None = None

    class Config:
        orm_mode = True


class UsersListElementModel(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str

    class Config:
        orm_mode = True
        from_attributes = True