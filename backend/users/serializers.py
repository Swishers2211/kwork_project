from django.utils.timezone import now

from rest_framework import serializers

from users.models import (
    User, 
    Interests, 
    Subscription,
)

from home.models import Video
from home.serializers import BaseVideoSerializer

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=60)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ['id', 'name', 'image_interest']

class ProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()  # Количество подписчиков
    subscriptions_count = serializers.SerializerMethodField()  # Количество подписок
    user_videos = serializers.SerializerMethodField()


    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'last_online', 'is_online', 'subscribers_count', 'subscriptions_count', 'user_videos']

    def get_is_online(self, obj):
        # Проверяем, был ли пользователь активен в последние 5 минут
        if obj.last_online and (now() - obj.last_online).total_seconds() < 300:  # 300 секунд = 5 минут
            return True
        return False

    def get_subscribers_count(self, obj):
        # Считаем количество записей в модели Subscription, где `target` — текущий пользователь
        return Subscription.objects.filter(target=obj).count()

    def get_subscriptions_count(self, obj):
        # Считаем количество записей в модели Subscription, где `subscriber` — текущий пользователь
        return Subscription.objects.filter(subscriber=obj).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance != request.user:
            data.pop('email', None)
        return data
    
    def get_user_videos(self, obj):
        videos = Video.objects.filter(author=obj)
        return BaseVideoSerializer(videos, many=True).data

class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.StringRelatedField()  # Имя подписчика
    target = serializers.StringRelatedField()  # Имя цели

    class Meta:
        model = Subscription
        fields = ['id', 'subscriber', 'target', 'created_at']