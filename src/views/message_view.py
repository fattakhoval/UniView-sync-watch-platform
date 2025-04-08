from pathlib import Path
from uuid import UUID

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import config
from src.db import get_db
from src.models import Message
from src.schemas import MessageOut


message_router = APIRouter(prefix='/messages')

@message_router.get('/room_messages/{room_id}')
async def get_messages(room_id: UUID, session: AsyncSession = Depends(get_db)):
    stmt = (
        select(Message)
        .where(Message.id_room == room_id)
        .options(selectinload(Message.user))
        .order_by(Message.created_at.asc())
    )
    result = await session.execute(stmt)
    messages = result.scalars().all()

    return [
        MessageOut(
            sender=msg.user.username,
            type='voice' if msg.is_voice else 'text',
            text=msg.message,
            voice_path=msg.voice_path,
            created_at=msg.created_at
        ) for msg in messages
    ]


@message_router.get('/voices/{voice_id}')
async def get_voice(voice_id: str):

    file_path = config.VOICE_DIR / Path(f'{voice_id}.webm')
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Voice message not found")
