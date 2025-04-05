from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


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
    type: str
    password: Optional[str] = ''
    live_time_room: Optional[datetime] = None


class RoomJoin1(BaseModel):

    id_room: UUID
    room_password: str

class RoomJoin(BaseModel):
    room_id: UUID
    password: str | None = None  # Пароль передается, если комната приватная


class RoomPasswordCheck(BaseModel):
    room_id: int
    password: str
