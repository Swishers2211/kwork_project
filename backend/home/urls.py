from django.urls import path

from home.views import (
    CreateVideoAPIView,
    VideosAPIView,
)

app_name = 'home'

urlpatterns = [
    path('api/create_video/', CreateVideoAPIView.as_view()),
    path('api/videos/', VideosAPIView.as_view()),
]
