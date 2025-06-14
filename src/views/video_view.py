import os
import re
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

import aiohttp

from config import config
from src.parsers.rutube_parser import ParserRutube
from src.parsers.vk_parser import ParserVK
from src.schemas import PlaylistRequest

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import FileResponse, JSONResponse


video_router = APIRouter(prefix='/video')


@video_router.get('/find_master_playlist/rutube/{video_id}')
async def find_master_playlist_rutube(video_id: str):
    parser = ParserRutube(video_id)
    await parser.launch_browser()
    res = await parser.run()
    await parser.close_browser()

    return JSONResponse(status_code=200 if res else 404, content={'link':res, 'type_src_video': 'rutube'})


@video_router.get('/find_master_playlist/vk')
async def find_master_playlist_rutube(link: str):
    parser = ParserVK(link)
    await parser.launch_browser()
    res = await parser.run()
    await parser.close_browser()

    return JSONResponse(status_code=200 if res else 404, content={'link':res, 'type_src_video': 'vk'})


@video_router.post("/playlist")
async def playlist(data: PlaylistRequest):

    async with aiohttp.ClientSession() as session:
        async with session.get(data.url,
                               headers={
                                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
                               }) as response:
            if response.status != 200:
                print('Ошибка')
                return Response(status_code=response.status)

            if data.type == 'vk':
                vk_url = urlparse(data.url)
                vk_domain = vk_url.netloc

            response_text = await response.text()
            new_data = ''

            for d in response_text.split('\n'):
                if d.startswith('#'):
                    new_data += d + '\n'
                else:
                    parsed = urlparse(d)
                    if data.type == 'rutube':
                        ori_domain = parsed.netloc

                    elif data.type == 'vk':
                        ori_domain = vk_domain

                    query_params = dict(parse_qsl(parsed.query))
                    query_params['ori_domain'] = ori_domain

                    if data.type == 'vk':
                        new_path = '/video/vk/segments_url' + parsed.path
                    else:
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


@video_router.get('/vk/segments_url/{path:path}')
async def get_segments_vk(path: str, request: Request):
    query_dict = dict(request.query_params)
    domain = query_dict.pop('ori_domain')

    replaced_url = f'http://127.0.0.1:8000/video/vk/video-segment'
    url = f'https://{domain}/{path}'

    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
    }) as session:
        async with session.get(url) as response:
            if response.status != 200:
                return Response(status_code=response.status)

            data = await response.text()
            new_data = ''

            for d in data.split('\n'):

                if d.startswith('#'):
                    new_data += d + '\n'
                else:
                    new_data += f'{replaced_url}/{path}/{d}?ori_domain={domain}\n'

            return Response(content=new_data, media_type="video/mp2t")


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


@video_router.get('/vk/video-segment/{path:path}')
async def get_segment_vk(path: str, request: Request):
    domain = request.query_params.get('ori_domain')
    url = f'https://{domain}/{path}'
    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'}) as client:
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
