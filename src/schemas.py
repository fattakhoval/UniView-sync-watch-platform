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

    title: str
    id_user: UUID
    room_type: str
    room_password: str
    live_time_room: Optional[datetime] = None


class RoomJoin(BaseModel):

    id_room: UUID
    room_password: str
