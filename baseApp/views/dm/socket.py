import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from baseApp.db.application.dm_models import Massage, DmRoom

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # ルームに参加
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # ルームから退出
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']
        user_id = self.scope['user'].id
        room_id = self.room_id

        # メッセージを保存
        room = DmRoom.objects.get(id=room_id)
        message = Massage(Room=room, Sender_id=user_id, Text=message_text)
        message.save()

        # グループの全メンバーにメッセージを送信
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'username': self.scope['user'].username,
            }
        )

    def chat_message(self, event):
        # WebSocketにメッセージを送信
        message = event['message']
        username = event['username']
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
