from backend.schemas.error import ErrorResponseSchema

# класс для переопределения ошибок
class ErrorResponseModel(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

