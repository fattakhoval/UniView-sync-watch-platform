from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.db import get_db
from src.jwt_utils import verify_password, hash_password, create_access_token
from src.models import User
from src.schemas import UserRegister, UserLogin

auth = APIRouter(prefix='/auth')


@auth.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.username.expression == user_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password):
        return JSONResponse(status_code=401, content="Incorrect username or password")

    access_token = create_access_token(data={"username": user.username, "id_user": str(user.id)})

    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)


@auth.post('/register')
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.username.expression == user_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        return JSONResponse(status_code=400, content="User already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    session.add(new_user)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "User created", "User": str(new_user)})

