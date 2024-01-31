from backend.src.exceptions.openapi_responses import user_not_auth_401, responses_error

# Дополнительные ответы для отображения в openapi

responses_base_users = {
    **user_not_auth_401,
    **responses_error(code=400, message="Вы сделали не правильный запрос, который отправили на сервер"),
}

responses_update_current_user = {
    **responses_error(code=404, message="Вы не найдены в системе")
}

