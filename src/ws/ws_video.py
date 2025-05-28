import time
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from config import config
from src.manager import video_manager, control_manager

ws_video_route = APIRouter()

@ws_video_route.websocket("/ws/video/{room_id}")
async def ws_video(room_id: UUID, websocket: WebSocket):
    await video_manager.connect(room_id, websocket)

    try:
        video_data = bytearray()

        while True:
            chunk = await websocket.receive_bytes()

            if chunk.startswith(b"LINK:"):
                link = chunk.decode()

                state = control_manager.video_state.get(room_id)

                if not state:
                    control_manager.video_state[room_id] = {
                        "timestamp": 0.0,
                        "status": "paused",
                        "link": link.split('LINK:')[1],
                        "updated_at": time.time(),
                        "master": control_manager.select_master(room_id)
                    }

                await video_manager.broadcast(room_id=room_id, message=link)
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
