from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.responses import JSONResponse

from src.db import get_db
from src.jwt_utils import hash_password, verify_password
from src.models import Room
from src.schemas import RoomCreate, RoomJoin
from src.ws.ws_chat import manager

room_router = APIRouter(prefix='/rooms')


@room_router.post('/create_room')
async def create_room(room_data: RoomCreate, session: AsyncSession = Depends(get_db)):

    new_room = Room(
        name=room_data.title,
        id_host=room_data.id_user,
        room_type=room_data.room_data,
        room_password=hash_password(room_data.room_password),
        live_time_room=room_data.live_time_room
    )

    session.add(new_room)
    await session.commit()

    manager.add_room(new_room.id)

    return JSONResponse(status_code=200, content={'message': 'Room created', 'Room': new_room})


@room_router.post('/join_room')
async def join_room(room_data: RoomJoin, session: AsyncSession = Depends(get_db)):
    stmt = select(Room).where(Room.id == room_data.id_room)
    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if not room or not verify_password(room_data.room_password, room.room_password):
        return JSONResponse(status_code=401, content='Incorrect password')

    return JSONResponse(status_code=200, content={'Join': 'Ok'})
