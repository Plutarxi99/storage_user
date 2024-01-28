from pydantic import BaseModel, EmailStr

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
