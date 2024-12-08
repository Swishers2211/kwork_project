import json
import base64
import os
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from channels.db import database_sync_to_async

from chat.models import (
    Room,
    Message,
    VoiceMessage
)
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
                        'username': chat_partner.username,
                    }
                }))
            elif self.other_user:
                other_user_instance = await database_sync_to_async(User.objects.get)(id=self.other_user)
                # Получаем или создаем комнату
                room_instance = await database_sync_to_async(Room.objects.filter(
                    Q(sender=self.user, receiver=other_user_instance) |
                    Q(sender=other_user_instance, receiver=self.user)
                ).first)()
                if room_instance:
                    self.chat_id = room_instance.id
                    self.room_group_name = f'chat_{self.chat_id}'
                    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                    await self.accept()
                    await self.send_chat_history()
                else:
                    await self.accept()
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
        message = text_data_json.get('message')
        image = text_data_json.get('image')  # base64
        video = text_data_json.get('video')  # base64
        voice_message = text_data_json.get('voice_message')  # base64
        message_action = text_data_json.get('message_action')
        user = self.scope['user']

        # Получаем или создаем комнату, если она не существует
        if not self.chat_id:
            self.room_group_name = await self.get_or_create_room()
            if self.room_group_name:
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                self.chat_id = int(self.room_group_name.split('_')[-1])

        if self.chat_id:
            # Обрабатываем действия с сообщениями
            if message_action == 'message_delete':
                message_id = text_data_json.get('message_id')
                if message_id:
                    result = await self.message_delete(message_id)
                    if result:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'message_deleted',
                                'message_id': message_id,
                            }
                        )
            elif message_action == 'message_edit':
                message_id = text_data_json.get('message_id')
                new_content = text_data_json.get('new_content')
                if message_id and new_content:
                    result = await self.message_edit(message_id, new_content)
                    if result:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'message_edited',
                                'message_id': message_id,
                                'new_content': new_content,
                            }
                        )
            else:
                # Декодируем и сохраняем файлы, если они есть
                image_path, video_path, voice_message_path = None, None, None

                if image:
                    image_binary = base64.b64decode(image)
                    image_path = os.path.join(settings.MEDIA_ROOT, 'messages/images', f'image_{user.id}.jpg')
                    os.makedirs(os.path.dirname(image_path), exist_ok=True)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_binary)
                    image_file_relative_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

                if video:
                    video_binary = base64.b64decode(video)
                    video_path = os.path.join(settings.MEDIA_ROOT, 'messages/videos', f'video_{user.id}.mp4')
                    os.makedirs(os.path.dirname(video_path), exist_ok=True)
                    with open(video_path, 'wb') as video_file:
                        video_file.write(video_binary)
                    video_file_relative_path = os.path.relpath(video_path, settings.MEDIA_ROOT)

                if voice_message:
                    voice_binary = base64.b64decode(voice_message)
                    voice_message_path = os.path.join(settings.MEDIA_ROOT, 'messages/voice_message', f'voice_{user.id}.mp3')
                    os.makedirs(os.path.dirname(voice_message_path), exist_ok=True)
                    with open(voice_message_path, 'wb') as voice_file:
                        voice_file.write(voice_binary)
                    voice_file_relative_path = os.path.relpath(voice_message_path, settings.MEDIA_ROOT)

                # Сохраняем сообщение
                message_instance = await self.save_message(
                    self.room_group_name,
                    user,
                    message,
                    image_path,
                    video_path,
                    voice_message_path
                )

                # Отправляем сообщение всем в группе
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'image': image_path,
                        'video': video_path,
                        'voice_message': voice_message_path,
                        'sender_id': user.id,
                        'sender_username': user.username,
                        'message_read': message_instance.message_read,
                    }
                )
        elif self.other_user:
            # Если есть другой пользователь, сохраняем сообщение
            image_path, video_path, voice_message_path = None, None, None

            if image:
                image_binary = base64.b64decode(image)
                image_path = os.path.join(settings.MEDIA_ROOT, 'messages/images', f'image_{user.id}.jpg')
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_binary)
                image_file_relative_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

            if video:
                video_binary = base64.b64decode(video)
                video_path = os.path.join(settings.MEDIA_ROOT, 'messages/videos', f'video_{user.id}.mp4')
                os.makedirs(os.path.dirname(video_path), exist_ok=True)
                with open(video_path, 'wb') as video_file:
                    video_file.write(video_binary)
                video_file_relative_path = os.path.relpath(video_path, settings.MEDIA_ROOT)

            if voice_message:
                voice_binary = base64.b64decode(voice_message)
                voice_message_path = os.path.join(settings.MEDIA_ROOT, 'messages/voice_message', f'voice_{user.id}.mp3')
                os.makedirs(os.path.dirname(voice_message_path), exist_ok=True)
                with open(voice_message_path, 'wb') as voice_file:
                    voice_file.write(voice_binary)
                voice_file_relative_path = os.path.relpath(voice_message_path, settings.MEDIA_ROOT)

            message_instance = await self.save_message(
                self.room_group_name,
                user,
                message,
                image_path,
                video_path,
                voice_message_path
            )

        # Отправляем сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'image': image_path,
                'video': video_path,
                'voice_message': voice_message_path,
                'sender_id': user.id,
                'sender_username': user.username,
                'message_read': message_instance.message_read,
            }
        )

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        Message.objects.filter(id=message_id).update(message_read=True)

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        message_read = event['message_read']

        # Если текущий пользователь — не отправитель, помечаем сообщение как прочитанное
        if sender_id != self.user.id:
            await self.mark_message_as_read(message_read=True)

        message_read_status = 'Да' if message_read else 'Нет'

        await self.send(text_data=json.dumps({
            'message': message,
            'message_read': message_read_status,
            'sender_id': sender_id,
            'sender_username': sender_username,
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        """Получаем или создаем комнату по пользователю-получателю и пользователю-отправителю"""
        try:
            other_user = User.objects.get(id=self.other_user)

            # Проверяем, существует ли уже комната между отправителем и получателем
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
    def save_message(self, room_group_name, user, message=None, image=None, video=None, voice_message=None):
        # Получаем ID комнаты из имени группы
        room_id = int(room_group_name.split('_')[-1])
        room = Room.objects.get(id=room_id)
        
        # Проверяем и сохраняем сообщения соответствующего типа
        if any([message, image, video]):
            return Message.objects.create(
                room=room,
                sender=user,
                message_text=message or '',
                message_image=image,
                message_video=video,
                message_read=False,
            )
        elif voice_message:
            return VoiceMessage.objects.create(
                room=room,
                sender=user,
                voice_message=voice_message,
                message_read=False,
            )
        else:
            raise ValueError("Необходимо передать хотя бы одно из значений: message, image, video или voice_message")

    async def send_chat_history(self):
        if self.chat_id:
            # Получаем объект комнаты
            room_instance = await database_sync_to_async(Room.objects.get)(id=self.chat_id)

            # Обновляем статус сообщений, помечая их как прочитанные
            await database_sync_to_async(
                Message.objects.filter(
                    room=room_instance,
                    message_read=False
                ).exclude(sender=self.user).update
            )(message_read=True)

            await database_sync_to_async(
                VoiceMessage.objects.filter(
                    room=room_instance,
                    message_read=False
                ).exclude(sender=self.user).update
            )(message_read=True)

            # Получаем текстовые и голосовые сообщения
            messages = await database_sync_to_async(list)(
                Message.objects.filter(room=room_instance).order_by('created_at')
            )
            voice_messages = await database_sync_to_async(list)(
                VoiceMessage.objects.filter(room=room_instance).order_by('created_at')
            )

            # Объединяем и сортируем сообщения по времени создания
            all_messages = sorted(
                messages + voice_messages,
                key=lambda msg: msg.created_at
            )

            # Сериализация объединённых сообщений
            serialized_messages = ListMessageSerializer(all_messages, many=True).data

            # Отправка истории сообщений
            await self.send(text_data=json.dumps({
                'history': serialized_messages,
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

    @database_sync_to_async
    def message_delete(self, message_id):
        try:
            message = (Message.objects.get(id=message_id, sender=self.user) | VoiceMessage.objects.get(id=message_id, sender=self.user)) 
            message.delete()
            return True
        except Message.DoesNotExist:
            return False
    
    async def message_deleted(self, event):
        message_id = event['message_id']

        await self.send(text_data=json.dumps({
            'message_action': 'message_delete',
            'message_id': message_id
        }))
    
    @database_sync_to_async
    def message_edit(self, message_id, new_content):
        try:
            message = Message.objects.get(id=message_id, sender=self.user)
            message.message_text = new_content
            message.save()
            return True
        except Message.DoesNotExist:
            return False
        
    async def message_edited(self, event):
        message_id = event['message_id']
        new_content = event['new_content']

        await self.send(text_data=json.dumps({
            'message_action': 'message_edit',
            'message_id': message_id,
            'new_content': new_content
        }))
