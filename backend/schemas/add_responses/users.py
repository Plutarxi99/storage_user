from backend.schemas.add_responses.base import get_cur_user_resp_200, user_not_auth_401, responses_error, \
    update_cur_user_resp_200

# Дополнительные ответы для отображения в openapi

responses_base_users = {
    **user_not_auth_401,
    **responses_error(code=400, message="Вы сделали не правильный запрос, который отправили на сервер"),
}

responses_update_current_user = {
    **responses_error(code=404, message="Вы не найдены в системе")
}

