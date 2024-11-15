from django.urls import re_path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/other_user/(?P<other_user>\w+)/$', ChatConsumer.as_asgi()),
]
