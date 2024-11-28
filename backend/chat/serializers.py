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
    message_type = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_message_read(self, obj):
        return 'Да' if obj.message_read else 'Нет'

    def get_message_type(self, obj):
        if hasattr(obj, 'message_text') and obj.message_text:
            return 'text'
        elif hasattr(obj, 'message_image') and obj.message_image:
            return 'image'
        elif hasattr(obj, 'message_video') and obj.message_video:
            return 'video'
        elif hasattr(obj, 'voice_message') and obj.voice_message:
            return 'voice'
        return 'unknown'

    def get_content(self, obj):
        if hasattr(obj, 'message_text') and obj.message_text:
            return obj.message_text
        elif hasattr(obj, 'message_image') and obj.message_image:
            return obj.message_image.url
        elif hasattr(obj, 'message_video') and obj.message_video:
            return obj.message_video.url
        elif hasattr(obj, 'voice_message') and obj.voice_message:
            return obj.voice_message.url
        return None

    class Meta(BaseMessageSerializer.Meta):
        fields = BaseMessageSerializer.Meta.fields + [
            'created_at', 'message_read', 'message_type', 'content',
        ]

class RoomsSerializer(BaseSerializer):
    sender = ProfileSerializer()
    receiver = ProfileSerializer()
    last_message_text = serializers.CharField(read_only=True)
    last_message_time = serializers.DateTimeField(format='%H:%M')

    class Meta(BaseSerializer.Meta):
        model = Room
        fields = BaseSerializer.Meta.fields + ['receiver', 'last_message_text', 'last_message_time']
