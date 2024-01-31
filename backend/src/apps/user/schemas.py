from datetime import date

from pydantic import BaseModel, EmailStr

from backend.src.operations.validators import PhoneNumberUser


# схемы для ответов и получения данных
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserAddDataBase(UserBase):
    first_name: str | None = "Луций"
    last_name: str | None = "Местрий"

    class Config:
        orm_mode = True
        from_attributes = True


class UserOtherDataBase(UserAddDataBase):
    other_name: str | None = "Плутарх"
    email: EmailStr
    phone: PhoneNumberUser | None = "+79123456789"
    birthday: date | None = "2007-11-07"

    class Config:
        orm_mode = True
        from_attributes = True


class UserSchema(UserOtherDataBase):
    id: int
    city: str | None = None
    additional_info: str | None = None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
        from_attributes = True


class CurrentUserResponseModel(UserOtherDataBase):
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUserModel(UserOtherDataBase):
    class Config:
        orm_mode = True


class UpdateUserResponseModel(UserOtherDataBase):
    id: int

    class Config:
        orm_mode = True


class UsersListElementModel(UserAddDataBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
