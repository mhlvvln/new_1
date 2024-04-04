from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from schemas import CreateUser, RegistrationConfirm, LoginUser, AuthCheck
from service import register_user, registration_confirm, auth, auth_check_code

auth_router = APIRouter()


@auth_router.post("/registration", tags=["Registration"], description="<h1>Регистрация пользователя</h1>"
                                                                      "<h4>"
                                                                      "Если эта почта есть и аккаунт подтвержден - работать не будет<br>"
                                                                      "Если почта есть и аккаунт не подтвержден - сработает с новыми данными(переданными в запросе)<br>"
                                                                      "После работы нужно подтвердить регистрацию<br>"
                                                                      "Пока не подтвердишь регистрацию - не будут работать методы авторизации<br>"
                                                                      "</h4>"
                                                                      "", summary="Регистрация")
async def registration(user: CreateUser, db: AsyncSession = Depends(get_session)):
    return await register_user(db, user)


@auth_router.post("/registration_confirm", summary="Подтверждение регистрации", tags=["Registration"])
async def registrationConfirm(data: RegistrationConfirm, db: AsyncSession = Depends(get_session)):
    return await registration_confirm(db, data)


@auth_router.post("/auth", tags=["Authorization"], summary="Запросить код авторизации")
async def auth_query(data: LoginUser, db: AsyncSession = Depends(get_session)):
    return await auth(db, data)


@auth_router.post("/auth_check", tags=["Authorization"], summary="Проверить код авторизации")
async def auth_check(data: AuthCheck, db: AsyncSession = Depends(get_session)):
    return await auth_check_code(db, data)


@auth_router.get("/get")
async def get():
    return {"get": True}