import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from home.models import (
    Video,
    Comment
)
from home.serializers import CommentSerializer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs'].get('video_id')

        # Получаем текущего пользователя
        self.user = self.scope['user']

        if self.user.is_authenticated:
            if self.video_id:
                # Пользователь подключается через chat_id
                self.room_group_name = f'video_{self.video_id}'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
                await self.send_comments_history()
            else:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.video_id:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        image = text_data_json.get('image')
        video = text_data_json.get('video')
        user = self.scope['user']

        if self.video_id:
            # Сохраняем сообщение и получаем его ID
            await self.save_message(self.room_group_name, user, message, image, video)

            # Отправляем сообщение всем в группе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_comment',
                    'message': message,
                    'author_id': user.id,
                    'author_username': user.username,
                }
            )

    async def video_comment(self, event):
        message = event['message']
        author_id = event['author_id']
        author_username = event['author_username']

        await self.send(text_data=json.dumps({
            'message': message,
            'author_id': author_id,
            'author_username': author_username,
        }))

    @database_sync_to_async
    def save_message(self, room_group_name, user, message=None, image=None, video=None):
        video_id = int(room_group_name.split('_')[-1])
        video = Video.objects.get(id=video_id)
        cmnt = Comment.objects.create(
            video=video,
            author=user,
            content=message if message else '',
            comment_image=image if image else '',
            comment_video=video if video else '',
        )
        return cmnt

    async def send_comments_history(self):
        if self.video_id:
            # Получаем видео через async обертку
            video_instance = await database_sync_to_async(Video.objects.get)(id=self.video_id)

            # Получаем комментарии асинхронно
            comments = await database_sync_to_async(list)(Comment.objects.filter(video=video_instance).order_by('-created_at'))

            # Сериализация комментариев асинхронно через database_sync_to_async
            comments_data = await database_sync_to_async(self.serialize_comments)(comments)

            await self.send(text_data=json.dumps({
                'history': comments_data,
            }))

    def serialize_comments(self, comments):
        return CommentSerializer(comments, many=True).data
