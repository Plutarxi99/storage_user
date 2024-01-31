from pydantic import BaseModel, EmailStr


# схемы для ответов и получения данных
class LoginModel(BaseModel):
    login: EmailStr
    password: str

