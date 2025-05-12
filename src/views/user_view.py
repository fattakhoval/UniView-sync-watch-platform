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

    user = await asession.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not exists")

    if data.email and data.email != user.email:
        stmt = select(User).where(User.email == data.email)
        result = await asession.execute(stmt)

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already in use")

        user.email = data.email

    if data.new_password:
        if not data.old_password:
            raise HTTPException(status_code=400, detail="Old password required to set a new password")
        if not verify_password(data.old_password, user.password):
            raise HTTPException(status_code=401, detail="Old password is incorrect")
        user.password = hash_password(data.new_password)

    await asession.commit()

    return JSONResponse(content=UserSchema.model_validate(user).model_dump(mode='json'), status_code=200)

@user_route.get("/info/{user_id}")
async def user_info(user_id: str, asession: AsyncSession = Depends(get_db)):
    user = await asession.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not exists")

    return JSONResponse(content=UserSchema.model_validate(user).model_dump(mode='json'), status_code=200)
