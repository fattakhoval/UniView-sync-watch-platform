from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import engine, Base, get_db
from src.manager import room_registry
from src.models import User
from src.routes import routers
from src.middleware import JWTAuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        async for session in get_db():
            await room_registry.load_rooms_from_db(session)
            #await User.create_bot(session)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)


[app.include_router(route) for route in routers]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(JWTAuthMiddleware)
