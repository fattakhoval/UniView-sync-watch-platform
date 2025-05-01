import os


from config import config

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse


video_router = APIRouter(prefix='/video')


@video_router.get("/{file_path}")
async def get_video(file_path: str):
    if not file_path.endswith('.webm'):
        file_path = f'{file_path}.webm'

    path = config.VIDEO_DIR / file_path
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content="File not found")

    return FileResponse(path, media_type="video/webm")