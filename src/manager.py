import json
import datetime

from uuid import UUID
from typing import List, Dict, Optional, Any, Set

from sqlalchemy import select
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Room


class RoomRegistry:
    def __init__(self):
        self.active_rooms: Set[UUID] = set()

    async def load_rooms_from_db(self, session: AsyncSession):
        result = await session.execute(
            select(Room.id).where(Room.live_time_room > datetime.datetime.now())
        )
        active_rooms = result.scalars().all()

        self.load_rooms(list(active_rooms))

        print(self.active_rooms)

    def load_rooms(self, rooms: list[UUID]):
        self.active_rooms.update(rooms)

    def is_room_active(self, room_id: UUID) -> bool:
        return room_id in self.active_rooms

    def add_room(self, room_id: UUID):
        self.active_rooms.add(room_id)

    def remove_room(self, room_id: UUID):
        self.active_rooms.discard(room_id)


class BaseManager:

    class RoomNotExists(Exception):

        @property
        def msg(self):
            return 'Room not exists; Check id room and retry again'

    def __init__(self, room_registry: RoomRegistry):
        self.room_registry = room_registry
        self.rooms: Dict[UUID, List[Optional[WebSocket]]] = {}

    async def connect(self, room_id: UUID, websocket: WebSocket):
        if room_id not in self.room_registry.active_rooms:
            raise self.RoomNotExists()

        if room_id not in self.rooms:
            self.rooms[room_id] = []

        await websocket.accept()
        self.rooms[room_id].append(websocket)

    def disconnect(self, room_id: UUID, websocket: WebSocket):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)

    def get_active_connections_count(self, room_id: UUID):
        connection = self.rooms.get(room_id, [])
        union = (set(con.user_id for con in connection))
        return len(union)

    def add_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = []

    async def broadcast(self, room_id: UUID, message: str):
        for connection in self.rooms.get(room_id, []):
            await connection.send_text(message)

class VideoManager(BaseManager):
    def __init__(self, room_registry: RoomRegistry):
        super().__init__(room_registry)
        self.video_state: Dict[UUID, Dict[str, Any]] = {}  # Храним текущее состояние видео

    async def update_video_state(self, room_id: UUID, state: Dict[str, Any]):
        self.video_state[room_id] = state
        await self.broadcast(room_id, json.dumps(state))

    async def broadcast_seek(self, room_id, seek_time):
        for websocket in self.rooms.get(room_id, []):
            try:
                await websocket.send_text(json.dumps({"action": f"seek:{seek_time}"}))
            except:
                pass


room_registry = RoomRegistry()

chat_manager = BaseManager(room_registry)
video_manager = VideoManager(room_registry)
control_manager = VideoManager(room_registry)
