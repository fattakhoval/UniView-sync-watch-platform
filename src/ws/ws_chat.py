import base64
import json
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from config import config
from src.db import get_db
from src.manager import chat_manager
from src.models import Message, User


ws_chat_route = APIRouter()


async def save_voice(room_id, username, filename, base64_data):
    async for session in get_db():
        user = await User.get_by_name(session=session, name=username)

        filepath = config.VOICE_DIR / f'{filename}.webm'

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(base64_data))

        new_message = Message(
            id_room=room_id,
            id_user=user.id,
            message=None,
            is_voice=True,
            voice_path=filename
        )
        session.add(new_message)
        await session.commit()

async def save_message(room_id, username, message):
    async for session in get_db():
        user = await User.get_by_name(session=session, name=username)

        new_message = Message(
            id_room=room_id,
            id_user=user.id,
            message=message
        )
        session.add(new_message)
        await session.commit()

@ws_chat_route.websocket("/ws/chat/{room_id}")
async def ws_chat(room_id: UUID, websocket: WebSocket):
    await chat_manager.connect(room_id, websocket)
    name = None
    try:
        while True:
            data = json.loads(await websocket.receive_text())
            name = data.get('sender')

            if data.get("type") == "voice":
                await save_voice(room_id, data["sender"], data['filename'], data["data"])
            else:
                await save_message(room_id, data["sender"], data["text"])

            await chat_manager.broadcast(room_id, json.dumps(data))

    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)
        await chat_manager.broadcast(room_id, f"Client `{name}` left the chat")
