import os
from datetime import timedelta, datetime
from random import randint

import sqlalchemy
from fastapi import HTTPException
from jose import jwt
from psycopg2 import IntegrityError
from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from exceptions import SuccessResponse
from models import User
from schemas import CreateUser, LoginUser, RegistrationConfirm, AuthCheck

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


async def getUserByPhone(session: AsyncSession, phone: str, role: str):
    result = await session.execute(select(User).filter(User.phone == phone, User.role == role).limit(1))
    return result.scalars().first()


async def getUserByEmail(session: AsyncSession, email: str, role: str):
    result = await session.execute(select(User).filter(User.email == email, User.role == role).limit(1))
    return result.scalars().first()


async def sendMail(mail: str):
    random_code = randint(111111, 111111)
    print(f"Выслали сообщение на почту {mail} с кодом {random_code}")
    return random_code


async def register_user(session: AsyncSession, user: CreateUser):
    check_user = await getUserByEmail(session, user.email, user.role)
    if check_user is not None and check_user.email_confirmed is True:
        raise HTTPException(status_code=403, detail="Пользователь уже зарегистрирован")

    if check_user is not None and check_user.email_confirmed is False:
        deleted = await session.execute(delete(User).where(User.id == check_user.id))
    random_code = await sendMail(user.email)
    new_user = User(first_name=user.first_name,
                    last_name=user.last_name,
                    patronymic=user.patronymic,
                    email=user.email,
                    code=random_code,
                    role=user.role,
                    photo=user.photo)
    session.add(new_user)
    try:
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(401, "email уже зарегистрирован")
    return SuccessResponse(data={"user": await new_user.to_dict()})


async def registration_confirm(db: AsyncSession, data=RegistrationConfirm):
    user = await getUserByEmail(db, data.email, data.role)
    if user is None:
        raise HTTPException(403, "Пользователя не существует, зарегистрируйтесь")
    if user.email_confirmed is True:
        return SuccessResponse(data={"error": "Неизвестная ошибка, обратитесь к Мише Вавилину"},
                               status_code=403,
                               status=False)

    if user.code == data.code:
        user.code = None
        user.email_confirmed = True
        data = {
            "id": user.id,
            "role": user.role,
        }
        access_token = await create_jwt_token(data)
        await db.commit()
        return SuccessResponse(data={"access_token": access_token, "data": data})
    else:
        raise HTTPException(status_code=401, detail="invalid code")


async def auth(db: AsyncSession, data: LoginUser):
    user = await getUserByEmail(db, data.email, data.role)
    if user is None:
        raise HTTPException(401, "Пройдите регистрацию, пользователя нет")
    if user.email_confirmed is False:
        raise HTTPException(401, "Пройдите регистрацию, подтвердите номер телефона")
    random_code = await sendMail(data.email)
    user.code = random_code
    await db.commit()
    return SuccessResponse()


async def auth_check_code(db: AsyncSession, data: AuthCheck):
    user = await getUserByEmail(db, data.email, data.role)
    if user is None:
        raise HTTPException(401, "Пройдите регистрацию, подтвердите номер телефона")
    if data.code == user.code:
        user.code = None
        data = {
            "id": user.id,
            "role": user.role,
        }
        access_token = await create_jwt_token(data)
        await db.commit()
        return SuccessResponse(data={"access_token": access_token, "data": data})
    else:
        raise HTTPException(401, "invalid code")


async def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(days=30000)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


"""
СДЕЛАТЬ РЕФРЕШ ТОКЕНА

ОТПРАВЛЯТЬ КОД ПО ПОЧТЕ
"""
