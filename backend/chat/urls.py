from django.urls import path

from chat.views import ListChatsAPIView

app_name = 'chat'

urlpatterns = [
    path('api/chats/', ListChatsAPIView.as_view()),
]
