import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


video_router = APIRouter(prefix='/video')


@video_router.get("/{file_path}")
async def get_video(file_path: str):
    new_path = 'temp_video/' + file_path
    if not os.path.exists(new_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(new_path, media_type="video/webm")