from pydantic import BaseModel

# схемы для ответов и получения данных
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None