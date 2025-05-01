import datetime

from sqlalchemy import select, and_

from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from src.db import get_db
from src.manager import room_registry
from src.models import Room, RoomType
from src.schemas import RoomCreate, RoomJoin, RoomOut
from src.ws.ws_chat import chat_manager
from src.ws.ws_action import control_manager
from src.ws.ws_video import video_manager
from src.jwt_utils import hash_password, verify_password

room_router = APIRouter(prefix='/rooms')


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

    room_registry.add_room(room_id=new_room.id)

    print(room_registry.active_rooms)
    return JSONResponse(status_code=200, content={'message': 'Room created', 'Room': {
        'id': str(new_room.id),
        'name': new_room.name,
        'type': new_room.room_type.value,
        'password': new_room.room_password,
        'id_host': str(new_room.id_host),
    }})




@room_router.post('/join_room')
async def join_room(room_data: RoomJoin, session: AsyncSession = Depends(get_db)):
    stmt = select(Room).where(Room.id == room_data.room_id)
    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if not room:
        return JSONResponse(status_code=404, content={'detail': 'Комната не найдена'})

    # Получаем пароль из тела запроса
    password = room_data.password

    # Если комната приватная и пароль не совпадает
    if room.room_type == RoomType.Private and not verify_password(password, room.room_password):
        return JSONResponse(status_code=401, content={'access': False, 'detail': 'Неверный пароль'})

    return JSONResponse(status_code=200, content={'access': True, 'room': {'id': str(room.id),
        'name': room.name,
        'type': room.room_type.value,
        'password': room.room_password,
        'id_host': str(room.id_host)}})


@room_router.get('/get_rooms')
async def get_rooms(session: AsyncSession = Depends(get_db)):
    stmt = select(Room).where(Room.live_time_room > datetime.datetime.now())
    result = (await session.execute(stmt)).all()
    result = [RoomOut(**list(res)[0].__dict__) for res in result]
    print(result)
    return result
