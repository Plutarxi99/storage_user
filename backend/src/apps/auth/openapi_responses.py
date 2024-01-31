from backend.src.exceptions.openapi_responses import get_cur_user_resp_200, responses_error

# Дополнительные ответы для отображения в openapi

responses_login = {
    **responses_error(code=401, message="Вас нет в системе"),
    **get_cur_user_resp_200
}
