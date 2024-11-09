import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import OuterRef, Subquery
from channels.db import database_sync_to_async

from django.db.models import Q

from chat.models import Room, Message
from users.models import User

from chat.serializers import ListMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs'].get('chat_id')
        self.other_user = self.scope['url_route']['kwargs'].get('other_user')

        # Получаем текущего пользователя
        self.user = self.scope['user']

        if self.user.is_authenticated:
            if self.chat_id:
                # Пользователь подключается через chat_id
                self.room_group_name = f'chat_{self.chat_id}'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
                await self.send_chat_history()
                chat_partner = await self.get_chat_partner()
                await self.send(text_data=json.dumps({
                    'chat_partner': {
                        'id': chat_partner.id,
                        'username': chat_partner.username
                    }
                }))
            elif self.other_user:
                other_user_instance = await database_sync_to_async(User.objects.get)(id=self.other_user)
                # Получаем или создаем комнату, где отправитель и получатель совпадают
                room_instance = await database_sync_to_async(Room.objects.filter(Q(sender=self.user, receiver=other_user_instance) | Q(sender=other_user_instance, receiver=self.user)).first)()
                if room_instance:
                    self.chat_id = room_instance.id
                    self.room_group_name = f'chat_{self.chat_id}'
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.accept()
                    await self.send_chat_history()
            else:
                # Если нет chat_id, пользователь подключается без комнаты
                await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.chat_id:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        image = text_data_json['image']
        user = self.scope['user']

        # Получаем или создаем комнату, если она не существует
        if not self.chat_id:
            self.room_group_name = await self.get_or_create_room()
            if self.room_group_name:
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                self.chat_id = int(self.room_group_name.split('_')[-1])

        if self.chat_id:
            # Сохраняем сообщение
            await self.save_message(self.room_group_name, user, message, image)
            await self.send_chat_history()

            # Отправляем сообщение всем в группе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': user.id,
                    'sender_username': user.username,
                }
            )
        else:
            await self.send_chat_history()

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_or_create_room(self):
        """Получаем или создаем комнату по продукту и пользователю-продавцу"""
        try:
            other_user = User.objects.get(id=self.other_user)

            # Проверяем, существует ли уже комната между пользователем и продавцом
            room = Room.objects.filter(sender=self.scope['user'], receiver=other_user).first()

            if room:
                self.chat_id = room.id
                return f'chat_{self.chat_id}'
            else:
                # Если комнаты нет, создаем новую
                room = Room.objects.create(sender=self.scope['user'], receiver=other_user)
                self.chat_id = room.id
                return f'chat_{self.chat_id}'

        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, room_group_name, user, message=None, image=None):
        room_id = int(room_group_name.split('_')[-1])
        room = Room.objects.get(id=room_id)
        Message.objects.create(room=room, sender=user, message_text=message if message else '', message_image=image if image else None)

    async def send_chat_history(self):
        if self.chat_id:
            room_instance = await database_sync_to_async(Room.objects.get)(id=self.chat_id)
            messages = await database_sync_to_async(list)(
                Message.objects.filter(room=room_instance).order_by('created_at')
            )
            await self.send(text_data=json.dumps({
                'history': ListMessageSerializer(messages, many=True).data,
            }))

    @database_sync_to_async
    def get_chat_partner(self):
        try:
            room = Room.objects.get(id=self.chat_id)
        except Room.DoesNotExist:
            return None

        if room.sender == self.user:
            return room.receiver
        else:
            return room.sender
