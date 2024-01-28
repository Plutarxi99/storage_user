from fastapi import APIRouter
from .endpoints import users, admin, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/private", tags=['admin'])
