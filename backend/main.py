from fastapi_pagination import add_pagination
from starlette.responses import JSONResponse

from backend.api.api_v1.api import api_router
from backend.db.session import engine, SessionLocal
from fastapi import FastAPI, Request, Response
from backend.db.session import Base
from fastapi.middleware.cors import CORSMiddleware

from backend.exceptions import ErrorResponseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
add_pagination(app)



@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.exception_handler(ErrorResponseModel)
async def unicorn_exception_handler(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.code,
        content=exc.message,
    )
