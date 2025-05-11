from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from config import config
from src.manager import video_manager

ws_video_route = APIRouter()

def get_id_from_chuck(chunk: str):

    if chunk.endswith('/'):
        chunk = chunk[:-1]

    return f'LINK:{chunk.split("/")[-1]}'

@ws_video_route.websocket("/ws/video/{room_id}")
async def ws_video(room_id: UUID, websocket: WebSocket):
    await video_manager.connect(room_id, websocket)

    try:
        video_data = bytearray()

        while True:
            chunk = await websocket.receive_bytes()

            if chunk.startswith(b"LINK:"):
                await video_manager.broadcast(room_id=room_id, message=chunk.decode())
                continue

            if chunk.startswith(b"__FILENAME__"):
                filename = chunk.decode().split(':')[1]
                if not filename.endswith('.webm'):
                    filename = f'{filename}.webm'

                await send(filename, video_data, video_manager.rooms.get(room_id, []))
                video_data.clear()
                continue

            video_data.extend(chunk)


    except WebSocketDisconnect:
        video_manager.disconnect(room_id, websocket)


async def send(filename, video_bytes, websockets):

    path = config.VIDEO_DIR / filename
    with open(path, 'wb') as file:
        file.write(video_bytes)

    for ws in websockets:
        await ws.send_text(f"{filename}")
