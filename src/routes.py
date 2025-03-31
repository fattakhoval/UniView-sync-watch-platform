import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/video/{video_id}")
async def get_video_by_id(video_id):
    video_path = f"/home/letquare/Downloads/{video_id}.mp4"
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        print('Нет файла')
        return {"error": "Video not found"}
