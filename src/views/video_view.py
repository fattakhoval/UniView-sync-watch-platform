import os
import re
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

import aiohttp

from config import config
from src.parsers.rutube_parser import Parser
from src.schemas import PlaylistRequest

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import FileResponse, JSONResponse


video_router = APIRouter(prefix='/video')


@video_router.get('/find_master_playlist/{video_id}')
async def find_master_playlist(video_id: str):
    parser = Parser(video_id)
    await parser.launch_browser()
    res = await parser.run()
    await parser.close_browser()

    return JSONResponse(status_code=200 if res else 404, content=res)


@video_router.post("/playlist")
async def playlist(data: PlaylistRequest):

    async with aiohttp.ClientSession() as session:
        async with session.get(data.url) as response:
            if response.status != 200:
                print('Ошибка')
                return Response(status_code=response.status)

            data = await response.text()
            new_data = ''

            for d in data.split('\n'):
                if d.startswith('#'):
                    new_data += d + '\n'
                else:
                    parsed = urlparse(d)
                    ori_domain = parsed.netloc

                    query_params = dict(parse_qsl(parsed.query))
                    query_params['ori_domain'] = ori_domain
                    new_path = '/video' + parsed.path

                    modified = parsed._replace(
                        scheme='http',
                        netloc='127.0.0.1:8000',
                        path=new_path,
                        query=urlencode(query_params)
                    )
                    new_url = urlunparse(modified)

                    new_data += new_url + '\n'

            return Response(content=new_data, media_type="application/vnd.apple.mpegurl")


@video_router.get("/hls-vod/{path:path}")
async def proxy_video(path: str, request: Request):

    query_dict = dict(request.query_params)
    domain = query_dict.pop('ori_domain')
    url = f'https://{domain}/hls-vod/{path}?{query_dict.get("i")}'

    path_segment = '/'.join(path.split('/')[:-1])
    url_segment = f'http://127.0.0.1:8000/video/video-segment/hls-vod/{path_segment}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return Response(status_code=response.status)

            data = await response.text()
            new_data = ''

            for d in data.split('\n'):

                if d.startswith('#'):
                    new_data += d + '\n'
                else:
                    new_data += url_segment + d + f'?ori_domain={domain}' + '\n'

            return Response(content=new_data, media_type="video/mp2t")


@video_router.get("/video-segment/{path:path}")
async def get_segment(path, request: Request):

    domain = request.query_params.get('ori_domain')
    url = f'https://{domain}/{path}'
    async with aiohttp.ClientSession() as client:
        resp = await client.get(url)
        if resp.status != 200:
            print('Error')
            return Response(status_code=resp.status)

        data = await resp.read()

    return Response(content=data, media_type="video/MP2T")


@video_router.get("/{file_path}")
async def get_video(file_path: str):
    if not file_path.endswith('.webm'):
        file_path = f'{file_path}.webm'

    path = config.VIDEO_DIR / file_path
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content="File not found")

    return FileResponse(path, media_type="video/webm")
