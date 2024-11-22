from django.utils.timezone import now

from rest_framework import serializers

from users.models import User

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

class ProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'last_online', 'is_online']

    def get_is_online(self, obj):
        # Проверяем, был ли пользователь активен в последние 5 минут
        if obj.last_online and (now() - obj.last_online).total_seconds() < 300:  # 300 секунд = 5 минут
            return True
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance != request.user:
            data.pop('email', None)
        return data
