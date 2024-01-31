from backend.src.exceptions.openapi_responses import responses_error, user_not_auth_401

# Дополнительные ответы для отображения в openapi

base_response_admin = {
    **responses_error(code=403, message="Вы не являетесь админом сервиса"),
    **responses_error(code=400, message="Вы сделали не правильный запрос на сервер"),
    **user_not_auth_401
}
