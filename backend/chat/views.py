from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, OuterRef, Subquery, DateTimeField
from django.core.cache import cache

from chat.models import Room, Message
from users.models import User
from chat.serializers import RoomsSerializer

class ListChatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        current_user_chats = Room.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver').order_by('-created_at')
        latest_messages = Message.objects.filter(room=OuterRef('pk')).order_by('-created_at')

        current_user_chats = current_user_chats.annotate(
            last_message_text=Subquery(latest_messages.values('message_text')[:1]),
            last_sender=Subquery(latest_messages.values('sender__username')[:1]),
            last_message_time=Subquery(latest_messages.values('created_at')[:1], output_field=DateTimeField())
        )

        # Сериализация данных
        data = RoomsSerializer(current_user_chats, many=True).data

        return Response({'current_user_chats': data, 'user_id': user}, status=status.HTTP_200_OK)
