from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from users.models import User
from home.models import Video, Comment

from home.serializers import (
    CategoryVideo,
    BaseVideoSerializer,
    CreateVideoSerializer,
    CommentSerializer
)

class VideosAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        videos = Video.objects.all()

        data = {'videos': BaseVideoSerializer(videos, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

class CreateVideoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateVideoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        try:    
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'message': 'Видео не найдено.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, video=video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, video_id):
        try:    
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'message': 'Видео не найдено.'}, status=status.HTTP_400_BAD_REQUEST)
        
        list_comments = Comment.objects.filter(video=video)
        data = {
            'video': BaseVideoSerializer(video).data,
            'list_comments': CommentSerializer(list_comments, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
