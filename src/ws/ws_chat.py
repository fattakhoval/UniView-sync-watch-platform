import base64
import json
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from config import config
from src.db import get_db
from src.bot_api import uniview_bot
from src.manager import chat_manager
from src.models import Message, User


ws_chat_route = APIRouter()


async def save_voice(room_id, username, filename, base64_data):
    async for session in get_db():
        user = await User.get_by_name(session=session, name=username)

        filepath = config.VOICE_DIR / f'{filename}'
        print(f'Try to save voice msg: {filepath}')
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

@ws_chat_route.websocket("/ws/chat/{room_id}/{user_id}")
async def ws_chat(room_id: UUID, user_id: UUID, websocket: WebSocket):
    websocket.user_id = user_id
    await chat_manager.connect(room_id, websocket)

    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data.get("type") == "voice":
                await save_voice(room_id, data["sender"], data['filename'], data["data"])
            else:
                await save_message(room_id, data["sender"], data["text"])

            await chat_manager.broadcast(room_id, json.dumps(data))

            if data.get('type') != 'voice' and data.get('text').startswith('!bot '):
                if uniview_bot.is_about_movies(data.get('text')):

                    request = data.get('text').split('!bot ')[1]
                    response = await uniview_bot.ask(request)

                    json_response = {
                        'sender': uniview_bot.name,
                        'type': 'text',
                        'text': response,
                        'voice_path': None
                    }
                    await save_message(room_id, uniview_bot.name, response)
                    await chat_manager.broadcast(room_id, json.dumps(json_response))
                else:
                    response = {
                        'sender': uniview_bot.name,
                        'type': 'text',
                        'text': uniview_bot.error_message,
                        'voice_path': None
                    }
                    await save_message(room_id, uniview_bot.name, uniview_bot.error_message)
                    await chat_manager.broadcast(room_id, json.dumps(response))

    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)
