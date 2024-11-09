from django.urls import path

from home.views import (
    AddCommentAPIView,
    CreateVideoAPIView,
    VideosAPIView,
)

app_name = 'home'

urlpatterns = [
    path('api/video_detail/<int:video_id>/', AddCommentAPIView.as_view()),
    path('api/create_video/', CreateVideoAPIView.as_view()),
    path('api/videos/', VideosAPIView.as_view()),
]
