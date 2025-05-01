from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.models import RoomType


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class RoomCreate(BaseModel):

    name: str
    id_user: UUID
    type: RoomType
    password: Optional[str] = ''
    live_time_room: Optional[datetime] = None


class RoomJoin(BaseModel):
    room_id: UUID
    password: str | None = None  # Пароль передается, если комната приватная


class RoomPasswordCheck(BaseModel):
    room_id: UUID
    password: str


class MessageOut(BaseModel):
    sender: str
    type: str
    text: str | None
    voice_path: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class RoomOut(BaseModel):
    name: str
    id_host: UUID
    room_type: RoomType
    live_time_room: Optional[datetime] = None