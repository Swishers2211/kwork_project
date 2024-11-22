from rest_framework import serializers

from chat.models import (
    Room,
    Message,
)

from users.serializers import ProfileSerializer

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'sender', 'receiver', 'created_at']
    
class CreateRoomSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Room

class BaseMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['room', 'sender', 'message_text']

class ListMessageSerializer(BaseMessageSerializer):
    created_at = serializers.DateTimeField(format="%H:%M")
    message_read = serializers.SerializerMethodField()

    def get_message_read(self, obj):
        return 'Да' if obj.message_read else 'Нет'

    class Meta(BaseMessageSerializer.Meta):
        fields = BaseMessageSerializer.Meta.fields + ['created_at', 'message_read']

class RoomsSerializer(BaseSerializer):
    sender = ProfileSerializer()
    receiver = ProfileSerializer()
    last_message_text = serializers.CharField(read_only=True)
    last_message_time = serializers.DateTimeField(format='%H:%M')

    class Meta(BaseSerializer.Meta):
        model = Room
        fields = BaseSerializer.Meta.fields + ['receiver', 'last_message_text', 'last_message_time']
