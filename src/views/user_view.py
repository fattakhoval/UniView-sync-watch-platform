import secrets

from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.jwt_utils import verify_password, hash_password
from src.models import User, ResetPasswordToken
from src.schemas import UpdateUser, UserSchema, RequirePassword, NewPassword
from src.smtp_module import send_recover_password

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


@user_route.post('/forgot_password')
async def forgot_password(require_data: RequirePassword, asession: AsyncSession = Depends(get_db)):

    user = await User.get_by_email(session=asession, email=require_data.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="Такого пользователя не существует")

    token = secrets.token_hex(16)

    try:
        new = ResetPasswordToken(
            id_user=user.id,
            token=token,
            email=require_data.email
        )

        asession.add(new)
        await asession.commit()

    except Exception:
        raise HTTPException(status_code=404, detail="Ошибка восстановления пароля, попробуйте позже:(")
    
    finally:
        await send_recover_password(user_data=user, token=token)
        return JSONResponse(content={'Send email': True}, status_code=200)

@user_route.get('/reset_password')
async def validation_reset_token(email: str, token: str, asession: AsyncSession = Depends(get_db)):

    if not await ResetPasswordToken.is_valid_token(session=asession, email=email, token=token):
        raise HTTPException(status_code=404, detail="НО НО НО мистер фиш, у вас не правильный токен")


    return RedirectResponse(url=f'https://uniview.space/resetpassword?email={email}&token={token}', status_code=303)


@user_route.post('/set_new_password')
async def set_new_password(data: NewPassword, asession: AsyncSession = Depends(get_db)):

    user = await User.get_by_email(session=asession, email=data.email)

    if not await ResetPasswordToken.is_valid_token(session=asession, email=data.email, token=data.token):
        raise HTTPException(status_code=404, detail="НО НО НО мистер фиш, у вас не правильный токен")

    if not user:
        raise HTTPException(status_code=404, detail="Такого пользователя не существует")

    user.password = hash_password(data.new_password)
    await asession.commit()

    await ResetPasswordToken.delete_token(session=asession, token=data.token)
    return JSONResponse(content={'Password update': True}, status_code=200)
