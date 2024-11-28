from rest_framework import serializers

from home.models import (
    Video, 
    CategoryVideo, 
    Comment,
    CommentVoice,
)
from users.models import User

class CategoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryVideo
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    comment_voice = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'comment_image', 'comment_video', 'comment_voice']

    def get_comment_voice(self, obj):
        # Проверяем наличие голосового комментария, связанного с данным объектом
        voice_comment = CommentVoice.objects.filter(video=obj.video, author=obj.author).first()
        if voice_comment:
            return {
                'id': voice_comment.id,
                'file': voice_comment.comment_voice.url,
                'created_at': voice_comment.created_at.strftime('%Y-%m-%d %H:%M')
            }
        return None

class BaseVideoSerializer(serializers.ModelSerializer):
    category_video = CategoryVideoSerializer()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Video
        fields = ['category_video', 'video_file', 'author', 'views_count', 'created_at', 'video_preview']

class CreateVideoSerializer(BaseVideoSerializer):
    class Meta(BaseVideoSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('views_count')
        data.pop('comments')
        return data
