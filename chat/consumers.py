import json
import asyncio
import threading

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.tasks import save_message

rutube_url = 'https://rutube.ru/play/embed/{uuid}'
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

        thread = threading.Thread(target=save_message, args=(message, self.chat_id, user_id))
        thread.start()

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

    async def receive(self, text_data=None, bytes_data=None):

        if bytes_data:
            await self.send_file(bytes_data)
        else:
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            print(action)
            match action:
                case 'new_link':
                    await self.send_link(text_data_json)

                case 'play':
                    await self.do_action('play')

                case 'pause':
                    await self.do_action('pause')

                case 'scroll':
                    await self.do_scroll(text_data_json['seek_time'])

    async def do_scroll(self, seek_time):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_scroll',
                'seek_time': seek_time,
            }
        )

    async def send_scroll(self, event):
        await self.send(text_data=json.dumps({
            'type': 'action',
            'do_action': 'scroll',
            'seek_time': event['seek_time']
        }))

    async def send_file(self, bytes_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_file',
                'file': bytes_data,
            }
        )

    async def add_file(self, event):
        await self.send(bytes_data=event['file'])

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
        split_url = url.split('/')
        video_id = split_url[-2] if split_url[-1] != '/' else split_url[-1]
        return rutube_url.format(uuid=video_id)

    @staticmethod
    def vkvideo_link(url: str):
        oid, id_ = url.split('/')[-1].split('-')[-1].split('_')
        return vkvideo_url.format(oid=oid, id_=id_)


    async def do_action(self, action):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'action_player',
                'do_action': action,
            }
        )

    async def action_player(self, event):
        await self.send(text_data=json.dumps({
            'type': 'action',
            'do_action': event['do_action']
        }))


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
