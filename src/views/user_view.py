from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.jwt_utils import verify_password, hash_password
from src.models import User
from src.schemas import UpdateUser, UserSchema

user_route = APIRouter(prefix="/user")


@user_route.put("/update_profile/{user_id}")
async def update_user(data: UpdateUser, user_id: str, asession: AsyncSession = Depends(get_db)):
    status = 200
    user = await asession.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователя не существует")

    if data.email and data.email != user.email:
        user.email = data.email
        status = 201

    if data.new_password:
        if not data.old_password:
            raise HTTPException(status_code=400, detail="Старый пароль обязателен для изменения пароля")
        if not verify_password(data.old_password, user.password):
            raise HTTPException(status_code=401, detail="Старый пароль неправильный")
        user.password = hash_password(data.new_password)
        status = 201

    await asession.commit()

    return JSONResponse(content=UserSchema.model_validate(user).model_dump(mode='json'), status_code=status)

@user_route.get("/info/{user_id}")
async def user_info(user_id: str, asession: AsyncSession = Depends(get_db)):
    user = await asession.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Такого пользователя не существует")

    return JSONResponse(content=UserSchema.model_validate(user).model_dump(mode='json'), status_code=200)
