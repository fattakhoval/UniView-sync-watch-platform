from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from src.manager import video_manager

ws_video_route = APIRouter()


@ws_video_route.websocket("/ws/video/{room_id}")
async def ws_video(room_id: str, websocket: WebSocket):
    await video_manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_bytes()
            for connection in video_manager.rooms.get(room_id, []):
                await connection.send_bytes(data)

    except WebSocketDisconnect:
        video_manager.disconnect(room_id, websocket)
