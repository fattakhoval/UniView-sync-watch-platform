import datetime
from uuid import UUID, uuid4
from typing import List

from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

from enum import Enum as PyEnum


class RoomType(PyEnum):
    Public = 'public'
    Private = 'private'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=True)
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC), nullable=False)

    messages: Mapped[List['Message']] = relationship()
    rooms: Mapped[List['Room']] = relationship()

    def __str__(self):
        return f'<User({self.username=}, {self.is_registered=}, {self.is_admin=})>'

    @property
    def display_name(self):
        return self.username if self.is_registered else f'Guest-{uuid4()}'


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_host: Mapped[UUID] = mapped_column(ForeignKey('users.id'), index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    room_type: Mapped[PyEnum] = mapped_column(Enum(RoomType), nullable=False, default=RoomType.Public)
    room_password: Mapped[str] = mapped_column(String(256), nullable=True)
    live_time_room: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    )

    message: Mapped['Message'] = relationship(back_populates="room")

    def __str__(self):
        return f'<Room({self.id=}, {self.name=}, {self.room_type=})>'

    def is_expired(self):
        return self.live_time_room < datetime.datetime.now(datetime.UTC)


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_room: Mapped[UUID] = mapped_column(ForeignKey('rooms.id'), index=True)
    id_user: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False, index=True)

    room: Mapped['Room'] = relationship(back_populates='message')
