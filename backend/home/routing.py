from django.urls import re_path

from home.cunsumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<video_id>\w+)/$', CommentConsumer.as_asgi()),
]
