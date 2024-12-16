import asyncio
import json
from urllib.parse import urljoin

import requests
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.tasks import save_message


rutube_url = 'https://rutube.ru/play/embed/{}'
vkvideo_url = 'https://vkvideo.ru/video_ext.php?oid=-{oid}&id={id_}'


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username, user_id = text_data_json['user'].split('@')

        save_message.delay(
            msg=message,
            chat_id=self.chat_id,
            user_id=user_id
        )

        # Отправка сообщения в группу комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Получение сообщения из группы комнаты
    async def chat_message(self, event):

        # Отправка сообщения в WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))


class RoomActionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.action_room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'action_{self.action_room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        match action:
            case 'new_link':
                await self.send_link(text_data_json)

    async def send_link(self, action_data):

        url = action_data['url']

        if 'rutube' in url:
            link = self.rutube_link(url)
        elif 'vkvideo' in url:
            link = self.vkvideo_link(url)
        else:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_link',
                'url': link,
            }
        )

    async def add_link(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'url': event['url']
        }))

    @staticmethod
    def rutube_link(url: str):
        video_id = url.split('/')[-1]
        return rutube_url.format(video_id)

    @staticmethod
    def vkvideo_link(url: str):
        oid, id_ = url.split('/')[-1].split('-')[-1].split('_')
        return vkvideo_url.format(oid=oid, id_=id_)


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'action_video'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        print('Ready to send')
        await asyncio.sleep(5)

        # Fetch and send video segments
        #for segment_content in get_video():
        for segment_content in jjk_video():
            if segment_content == 'END_OF_STREAM':
                await self.send('END_OF_STREAM')  # Notify the client that the stream has ended
                break
            else:
                convert = transcode_segment(segment_content)
                await self.send(convert)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, bytes_data):
        await self.send(bytes_data)


def get_video():
    import m3u8
    import requests

    url = 'https://river-3-335.rutube.ru/hls-vod/9UVEimcMVXKcA8aj3UYrVA/1734975692/2317/rutube-ds-origin-vs322-1/21ca585aa2b04478aeaafdda793d8036.mp4.m3u8?i=1280x692_889'

        # Fetch the M3U8 playlist
    response =  requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails
    playlist = m3u8.loads(response.text)

    # Get the base URL for resolving relative segment URLs
    base_url = url.rsplit('/', 1)[0] + '/'

    # Iterate over the segments in the playlist
    for segment in playlist.segments:
        segment_url = urljoin(base_url, segment.uri)  # Resolve the full URL of the segment
        print(f"Fetching segment: {segment_url}")

        # Fetch the segment content
        try:
            segment_response = requests.get(segment_url)
            segment_response.raise_for_status()
            yield segment_response.content  # Yield the segment content
        except Exception as e:
            print(f"Failed to fetch segment: {segment_url}, error: {e}")

    # Notify that the stream has ended
    yield 'END_OF_STREAM'


def transcode_segment(segment):
    import ffmpeg

    # Create a process to transcode the input segment
    process = (
        ffmpeg
        .input('pipe:0', format='mp4')  # Input format is MPEG-TS (mpegts)
        .output('pipe:1', format='webm', vcodec='libvpx', acodec='libvorbis')  # Output format is WebM
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    # Run the process and send the segment data to stdin
    output, error = process.communicate(input=segment)

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {error.decode()}")

    return output

def jjk_video():

    chunk_size = 1024 * 1024
    video_file = '/home/letquare/Downloads/Jujutsu Kaisen Season 2「AMV」After Dark x Sweater Weather.mp4'

    with open(video_file, 'rb') as video_file:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break  # End of file reached

            print(f'send: {len(chunk)}')
            yield chunk

        yield 'END_OF_STREAM'