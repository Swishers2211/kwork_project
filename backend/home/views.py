from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import (
    User,
    Subscription
)
from home.models import (
    Video, 
    Comment
)
from home.serializers import (
    CategoryVideo,
    BaseVideoSerializer,
    CreateVideoSerializer,
)

class VideosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Лента видео",
        operation_description="Возвращает ленту видео, включая все видео и видео от подписок.",
        responses={
            200: openapi.Response(
                description="Список видео",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'all_videos': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(  # Используем items для массива
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID видео"),
                                        }
                                    ),
                                    'category_video': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID категории видео"),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название категории видео")
                                        }
                                    ),
                                    'video_file': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к видеофайлу"
                                    ),
                                    'author': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID автора"),
                                            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя автора")
                                        }
                                    ),
                                    'views_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество просмотров видео"
                                    ),
                                    'created_at': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        description="Дата и время создания видео (формат: 'YYYY-MM-DD HH:MM')"
                                    ),
                                    'video_preview': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к превью видео"
                                    ),
                                }
                            )
                        ),
                        'subscribed_videos': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(  # Используем items для массива
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID видео"),
                                        }
                                    ),
                                    'category_video': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID категории видео"),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название категории видео")
                                        }
                                    ),
                                    'video_file': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к видеофайлу"
                                    ),
                                    'author': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID автора"),
                                            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя автора")
                                        }
                                    ),
                                    'views_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество просмотров видео"
                                    ),
                                    'created_at': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        description="Дата и время создания видео (формат: 'YYYY-MM-DD HH:MM')"
                                    ),
                                    'video_preview': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к превью видео"
                                    ),
                                }
                            )
                        ),
                    }
                )
            ),
        },
    )
    def get(self, request):
        user = request.user

        # Получаем все видео
        all_videos = Video.objects.all()

        # Получаем видео пользователей, на которых подписан текущий пользователь
        subscriptions = Subscription.objects.filter(subscriber=user).values_list('target', flat=True)
        subscribed_videos = Video.objects.filter(author__id__in=subscriptions)

        # Формируем ответ
        data = {
            "all_videos": BaseVideoSerializer(all_videos, many=True).data,
            "subscribed_videos": BaseVideoSerializer(subscribed_videos, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class CreateVideoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateVideoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
