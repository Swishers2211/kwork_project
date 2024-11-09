from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import authenticate

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from users.models import User
from users.serializers import (
    RegisterSerializer, 
    ProfileSerializer, 
)

class CheckAuthAPIView(APIView): # Класс проверки авторизован ли пользователь или нет
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_authenticated:
                user_id = request.user.id
                return Response({'isAuthenticated': True, 'user_id': user_id, 'user': request.user.username})
        else:
            return Response(
                {'message': 'Сначала авторизуйтесь!'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterAPIView(APIView): # Класс для регистрации аккаунта
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(user): # функция для генерациии токена при логине пользователя в системе
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginAPIView(APIView): # Класс для входа в систему
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password) # если введенные данные есть в базе, то логинем

        if user is None:
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        data = get_tokens_for_user(user) # генерация токена
        response = Response(data)

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value=data['access'], 
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], 
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'], 
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'], 
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        ) # Ложим токен в куки
        csrf.get_token(request) # Получаем csrf_token

        return response
    
    def get(self, request):
        return Response({'detail': 'auth'})

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class DashboardAPIView(APIView): # Профиль пользователя
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.filter(pk=user_id).first() # Получаем текущего пользователя

        if not user:
            return Response({'detail': 'Пользователь не найден'}, status=404)

        serializer = ProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

class LogoutAPIView(APIView): # Класс для выхода из системы
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token") # Получаем refresh_token для дальнейшего занесения его в чс
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist() # Заносим токен в чс
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Успешный выход!'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE']) # Удаляем куки
        return response

class ListUserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        list_user = User.objects.all()

        data = {'list_user': ProfileSerializer(list_user, many=True).data}
        return Response(data, status=status.HTTP_200_OK)
