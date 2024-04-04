from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from database.database import init_models
from router import auth_router

app = FastAPI(title="APIServer", description="<h1>"
                                             "Swagger for API"
                                             "</h1>"
                                             "<h4>"
                                             "Сервер разбит на авторизазацию и регистрацию<br>"
                                             "После регистрации нужно подтвердить почту<br>"
                                             "Если этого не сделать, то успеха не будет<br>"
                                             "После подтверждения регистрации будет получен токен<br>"
                                             "Дальше на этом аккаунте получить токен через регистрацию будет нельзя<br>"
                                             "Получать придется только методами авторизации<br>"
                                             "</h4>"
                                             ""
                                             "")

app.include_router(auth_router, prefix="/auth")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "error": exc.detail},
    )


@app.on_event("startup")
async def startup():
    await init_models()