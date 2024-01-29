import phonenumbers
from pydantic import BaseModel, EmailStr, field_validator


# схемы для ответов и получения данных
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserAddDataBase(UserBase):
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True


class UserOtherDataBase(UserAddDataBase):
    other_name: str | None = None
    email: EmailStr
    phone: str | None = None
    birthday: str | None = None

    # валидация номера телефона
    @field_validator('phone')
    @classmethod
    def check_phone(cls, v: str) -> str:
        try:
            # если номер начинается с "+", то переходит к следующему условию
            if v[0] == "+":
                int(v[1:])
            phonenumbers.parse(v, None)
            return v
        except:
            raise ValueError(f'Не правильно набран номер{v}')

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
