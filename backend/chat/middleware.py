from jwt import decode as jwt_decode
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
from users.models import User
from rest_framework_simplejwt.exceptions import InvalidToken

@database_sync_to_async
def get_user_from_jwt(token):
    try:
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=decoded_data['user_id'])
        return user
    except (InvalidToken, User.DoesNotExist):
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Извлечение токена из cookies
        cookies = scope['headers']
        token = None
        for header in cookies:
            if header[0] == b'cookie':
                cookies_str = header[1].decode()
                cookies_dict = dict(x.split('=') for x in cookies_str.split('; '))
                token = cookies_dict.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        # Проверка токена и установка пользователя
        scope['user'] = await get_user_from_jwt(token) if token else AnonymousUser()

        return await super().__call__(scope, receive, send)
