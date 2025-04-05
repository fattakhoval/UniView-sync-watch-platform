from sqlalchemy import select
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models import Room, RoomType
from src.schemas import RoomCreate, RoomJoin
from src.ws.ws_chat import chat_manager
from src.ws.ws_action import control_manager
from src.ws.ws_share_video import video_manager
from src.jwt_utils import hash_password, verify_password

room_router = APIRouter(prefix='/rooms')


def init_room_settings(room_id):
    video_manager.add_room(room_id)
    chat_manager.add_room(room_id)
    control_manager.add_room(room_id)


@room_router.post('/create_room')
async def create_room(room_data: RoomCreate, session: AsyncSession = Depends(get_db)):

    new_room = Room(
        name=room_data.name,
        id_host=room_data.id_user,
        room_type=room_data.type,
        room_password=hash_password(room_data.password) if room_data.password else None,
        live_time_room=room_data.live_time_room
    )

    session.add(new_room)
    await session.commit()

    init_room_settings(str(new_room.id))

    return JSONResponse(status_code=200, content={'message': 'Room created', 'Room': {
        'id': str(new_room.id),
        'name': new_room.name,
        'type': new_room.room_type.value,
        'password': new_room.room_password,
    }})


@room_router.post('/join_room')
async def join_room(room_data: RoomJoin, session: AsyncSession = Depends(get_db)):
    stmt = select(Room).where(Room.id == room_data.room_id)
    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if not room:
        return JSONResponse(status_code=404, content={'detail': 'Комната не найдена'})

    if room.room_type == RoomType.Private and not verify_password(room_data.password, room.room_password):
        return JSONResponse(status_code=401, content={'access': False, 'detail': 'Неверный пароль'})

    return JSONResponse(status_code=200, content={'access': True})
