from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect


from src.manager import video_manager

ws_video_route = APIRouter()


@ws_video_route.websocket("/ws/video/{room_id}")
async def ws_video(room_id: UUID, websocket: WebSocket):
    await video_manager.connect(room_id, websocket)

    try:

        print(f"[Room {room_id}] Accepting file...")
        video_data = bytearray()

        while True:
            chunk = await websocket.receive_bytes()
            if chunk.endswith(b"__END_OF_STREAM__"):
                await send(video_data, video_manager.rooms.get(room_id, []))
                continue
            video_data.extend(chunk)


    except WebSocketDisconnect:
        video_manager.disconnect(room_id, websocket)


async def send(video_bytes, websockets):

    filename = 'video.webm'
    with open(f'temp_video/{filename}', 'wb') as file:
        file.write(video_bytes)

    for ws in websockets:
        await ws.send_text(f"Video path: /{filename}")
