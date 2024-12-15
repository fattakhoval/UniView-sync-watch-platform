import json

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
