import asyncio
import math
import os
import subprocess
import tempfile
import ffmpeg
import uuid
from io import BytesIO
from pathlib import Path
import shlex
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
                await segment_and_send(video_data, room_id, video_manager.rooms.get(room_id, []))
                continue
            video_data.extend(chunk)


    except WebSocketDisconnect:
        video_manager.disconnect(room_id, websocket)


async def segment_and_send(video_bytes, room_id, websocket, split_length=10):

    filename = 'video.webm'
    with open(f'temp_video/{filename}', 'wb') as file:
        file.write(video_bytes)

    for ws in websocket:
        await ws.send_text(f"Video path: /{filename}")

    print(f"[Room {room_id}] Done sending all segments.")



def get_video_length(filename):
    probe = ffmpeg.probe(filename)
    duration = float(probe['format']['duration'])
    print(f"Video length in seconds: {duration}")
    return int(duration)

def ceildiv(a, b):
    return int(math.ceil(a / float(b)))

