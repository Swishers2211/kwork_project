from django.db.models import Q, OuterRef, Subquery, DateTimeField, Case, When, Value, CharField
from chat.models import Room, Message, VoiceMessage
from chat.serializers import RoomsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ListChatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id

        # Получаем чаты текущего пользователя
        current_user_chats = Room.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('-created_at')

        # Подзапросы для последних сообщений
        latest_messages = Message.objects.filter(room=OuterRef('pk')).order_by('-created_at')
        latest_voice_messages = VoiceMessage.objects.filter(room=OuterRef('pk')).order_by('-created_at')

        # Агрегация данных о последнем сообщении (текст, медиа, голос)
        current_user_chats = current_user_chats.annotate(
            last_message_text=Subquery(latest_messages.values('message_text')[:1]),
            last_message_image=Subquery(latest_messages.values('message_image')[:1]),
            last_message_video=Subquery(latest_messages.values('message_video')[:1]),
            last_voice_message=Subquery(latest_voice_messages.values('voice_message')[:1]),
            last_sender=Subquery(latest_messages.values('sender__username')[:1]),
            last_message_time=Subquery(
                latest_messages.values('created_at')[:1],
                output_field=DateTimeField()
            ),
            last_message_type=Case(
                When(last_message_text__isnull=False, then=Value('text')),
                When(last_message_image__isnull=False, then=Value('image')),
                When(last_message_video__isnull=False, then=Value('video')),
                When(last_voice_message__isnull=False, then=Value('voice')),
                default=Value('unknown'),
                output_field=CharField()
            )
        )

        # Сериализация данных
        data = RoomsSerializer(current_user_chats, many=True).data

        return Response({'current_user_chats': data, 'user_id': user}, status=status.HTTP_200_OK)
