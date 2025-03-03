from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin():
        await engine.run_sync()

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)
