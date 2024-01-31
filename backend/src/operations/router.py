from fastapi import APIRouter

from backend.src.apps.auth.endpoints import router_auth
from backend.src.apps.admin.endpoints import router_admin
from backend.src.apps.user.endpoints import router_user

# соединения эндпоинтов для включения их в сервис
api_router = APIRouter()
api_router.include_router(router_auth, tags=['auth'])
api_router.include_router(router_user, prefix="/users", tags=["users"])
api_router.include_router(router_admin, prefix="/private", tags=['admin'])
