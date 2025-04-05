from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from src.manager import chat_manager

ws_chat_route = APIRouter()


@ws_chat_route.websocket("/ws/chat/{room_id}")
async def ws_chat(room_id: str, websocket: WebSocket):
    await chat_manager.connect(room_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await chat_manager.broadcast(room_id, message)

    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)
        await chat_manager.broadcast(room_id, f"Client # left the chat")
