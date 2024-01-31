import pathlib

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination
from starlette.responses import JSONResponse

from backend.src.operations.router import api_router
from backend.src.database import engine, SessionLocal
from fastapi import FastAPI, Request, Response
from backend.src.database import Base

from backend.src.exceptions.model import ErrorResponseModel
from backend.src.exceptions.schemas import ErrorResponseSchema
from alembic.config import Config
from alembic import command

from .core.config import settings

Base.metadata.create_all(bind=engine)
file_alembic = pathlib.Path(__file__).parent.parent.joinpath("alembic.ini")
alembic_cfg = Config(file_alembic)
alembic_cfg.set_main_option("script_location", "backend/migrations")
alembic_cfg.set_main_option("sqlalchemy.url", f"{settings.SQLALCHEMY_DATABASE_URI}")
# command.stamp(alembic_cfg, "head")
command.upgrade(alembic_cfg, "head")
app = FastAPI()
app.include_router(api_router)
add_pagination(app)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Возвращает подключение к базе данных, пока используется, иначе закрывает подключение
    """
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.exception_handler(ErrorResponseModel)
async def bad_request_400(request: Request, exc: ErrorResponseModel):
    """
    Отлов ошибок и отправка в виде json пользователю
    """
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder(ErrorResponseSchema(code=exc.code, message=exc.message)),
    )
