from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.db import engine, Base
from src.routes import router
from src.views.view_room import room_router
from src.ws.ws_chat import app_ws
from src.views.auth_view import auth
from src.middleware import JWTAuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.options('/test')
async def optional_test():
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )

@app.get('/test')
async def get():

    return {'ok': 'ok'}




app.include_router(router)
app.include_router(app_ws)
app.include_router(auth)
app.include_router(room_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(JWTAuthMiddleware)
