from rest_framework import serializers

from home.models import Video, CategoryVideo, Comment
from users.models import User

class CategoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryVideo
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Comment
        fields = ['author', 'content', 'created_at']

class BaseVideoSerializer(serializers.ModelSerializer):
    category_video = CategoryVideoSerializer()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Video
        fields = ['category_video', 'video_file', 'author', 'views_count', 'created_at']

class CreateVideoSerializer(BaseVideoSerializer):
    class Meta(BaseVideoSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('views_count')
        data.pop('comments')
        return data
