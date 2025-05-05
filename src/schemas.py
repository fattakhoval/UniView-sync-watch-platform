from typing import Optional
from uuid import UUID
from datetime import datetime, date, time

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
    id: UUID
    name: str
    count: int
    id_host: UUID
    room_type: RoomType
    live_time_room: Optional[datetime] = None


class FriendPending(BaseModel):
    id: UUID
    username: str
    status: str

    class Config:
        from_attributes = True


class Friend(BaseModel):
    id: UUID
    username: str
    email: str

    class Config:
        from_attributes = True


class EventCreate(BaseModel):

    id_creator: UUID
    title: str
    invited_list: list[UUID]
    date: date
    time: time

class EventOut(BaseModel):

    id: UUID
    id_creator: UUID
    id_room: Optional[UUID]
    title: str
    datetime_start: datetime
