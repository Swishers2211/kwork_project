from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

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
