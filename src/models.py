import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, UTC, timedelta
from src.db import Base

from enum import Enum as PyEnum


class RoomType(PyEnum):
    XS = 4
    S = 8
    M = 12
    L = 16
    XL = 20
    XXL = 24


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(256), nullable=True)
    is_registered = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_host = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)


    def __str__(self):
        return f"<User(id={self.id}, username={self.name}, is_registered={self.is_registered}, is_admin={self.is_admin}, is_host={self.is_host})>"

    @property
    def display_name(self):
        return self.username if self.is_registered else f"Guest-{self.id}"


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(256), nullable=False)
    slag = Column(String(256), unique=True, nullable=False)
    room_type = Column(Enum(RoomType), nullable=False, default=RoomType.XS)
    live_time_room = Column(DateTime, nullable=False, default=datetime.now(UTC) + timedelta(days=1))

    def __str__(self):
        return f"<Room(id={self.id}, name={self.name}, slag={self.slag}, room_type={self.room_type})>"

    def is_expired(self):
        return self.live_time_room < datetime.now(UTC)

class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(256), nullable=False)
    url = Column(Text, nullable=False)
    home_url = Column(String(200), nullable=False)
    is_our = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
