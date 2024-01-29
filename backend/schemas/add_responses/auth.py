from backend.schemas.add_responses.base import get_cur_user_resp_200, responses_error
from backend.schemas.error import ErrorResponseSchema
from backend.schemas.user import CurrentUserResponseModel

responses_login = {
    **responses_error(code=400, message="Вас нет в системе"),
    **get_cur_user_resp_200
}
