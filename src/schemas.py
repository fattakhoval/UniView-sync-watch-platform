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
    username: str # 43612ba5-7c67-4474-95f0-71865fc6d823
    password: str # qwe


class RoomCreate(BaseModel):
    name: str
    id_user: UUID
    type: RoomType
    password: Optional[str] = ''
    live_time_room: Optional[datetime] = None


class RoomJoin(BaseModel):
    room_id: UUID # 16576bdf-ce23-44c0-8239-74f9d68c7c3e
    password: str | None = None
