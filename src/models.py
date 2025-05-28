import datetime
from uuid import UUID, uuid4
from typing import List, Optional

from sqlalchemy import String, DateTime, Enum, Text, ForeignKey, Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import config
from src.db import Base

from enum import Enum as PyEnum


class RoomType(PyEnum):
    Public = 'public'
    Private = 'private'


class UserRole(PyEnum):
    User = 'user'
    Admin = 'admin'
    Bot = 'bot'


class FriendshipStatus(PyEnum):
    Pending = 'pending'
    Accepted = 'accepted'
    Declined = 'declined'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=True)
    role: Mapped[PyEnum] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.User)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now, nullable=False)

    messages: Mapped[List['Message']] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    rooms: Mapped[List['Room']] = relationship(
        back_populates="host",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __str__(self):
        return f'<User({self.username=}, {self.role=})>'

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str):
        stmt = select(cls).where(cls.username == name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create_bot(cls, session: AsyncSession):
        new_bot = cls(
            id=UUID(config.BOT_UUID),
            username='UniViewBOT',
            email='empty',
            password=str(uuid4()),
            role=UserRole.Bot
        )
        try:
            session.add(new_bot)
            await session.commit()
        except IntegrityError as exc:
            print(exc)

        finally:
            return None


def default_live_time():
    return datetime.datetime.now() + datetime.timedelta(days=1)


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_host: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    room_type: Mapped[PyEnum] = mapped_column(Enum(RoomType), nullable=False, default=RoomType.Public)
    room_password: Mapped[str] = mapped_column(String(256), nullable=True)
    live_time_room: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=default_live_time
    )

    messages: Mapped[List['Message']] = relationship(
        back_populates="room",
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    host: Mapped['User'] = relationship(back_populates='rooms')

    def __str__(self):
        return f'<Room({self.id=}, {self.name=}, {self.room_type=})>'


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_room: Mapped[UUID] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'), index=True)
    id_user: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    message: Mapped[str] = mapped_column(Text, nullable=True)
    is_voice: Mapped[bool] = mapped_column(Boolean, default=False)
    voice_path: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False, index=True)

    room: Mapped['Room'] = relationship(back_populates='messages', passive_deletes=True)
    user: Mapped['User'] = relationship(back_populates='messages', passive_deletes=True)


class Friendship(Base):
    __tablename__ = 'friendships'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_requester: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    id_addressee: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    status: Mapped[PyEnum] = mapped_column(Enum(FriendshipStatus), nullable=False, default=FriendshipStatus.Pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)

    requester = relationship('User', foreign_keys=[id_requester], passive_deletes=True)
    addressee = relationship('User', foreign_keys=[id_addressee], passive_deletes=True)


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_creator: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    id_room: Mapped[Optional[UUID]] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'), nullable=True)
    title: Mapped[str] = mapped_column(String(128))
    datetime_start: Mapped[datetime] = mapped_column(DateTime)
    is_second_msg_send: Mapped[bool] = mapped_column(Boolean, default=False)

    invites: Mapped[List['Invite']] = relationship(
        'Invite',
        back_populates='event',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Invite(Base):
    __tablename__ = 'invites'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    id_event: Mapped[UUID] = mapped_column(ForeignKey('events.id', ondelete='CASCADE'))
    id_inviter: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    id_invited: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    event = relationship('Event', back_populates='invites', passive_deletes=True)
