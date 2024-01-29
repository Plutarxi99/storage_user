from pydantic import BaseModel, EmailStr
# схемы для ответов и получения данных
class LoginModel(BaseModel):
    login: str
    password: str

# class EmailValidate(EmailStr):
#     login: str
#
#
# class LoginModel(BaseModel):
#     login: EmailValidate
#     password: str
