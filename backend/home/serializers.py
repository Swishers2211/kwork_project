from rest_framework import serializers

from home.models import (
    Video, 
    CategoryVideo, 
    Comment,
    CommentVoice,
)

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
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'category_video', 'video_file', 'author', 'author_id', 'views_count', 'created_at', 'video_preview']

class CreateVideoSerializer(BaseVideoSerializer):
    category_video = serializers.PrimaryKeyRelatedField(queryset=CategoryVideo.objects.all())
    
    class Meta(BaseVideoSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('id')
        data.pop('views_count')
        data.pop('author_id')
        return data
