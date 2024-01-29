from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    code: int
    message: str
