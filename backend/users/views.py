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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import (
    User,
    Subscription,
    Interests,
)
from users.serializers import (
    RegisterSerializer, 
    ProfileSerializer, 
    InterestSerializer,
)

class CheckAuthAPIView(APIView): # Класс проверки авторизован ли пользователь или нет
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Проверка на аутентификацию',
        operation_description='Проверяет на стороне бекенда, аутентифицирован пользователь или нет',
        responses={
            200: openapi.Response(
                description="Пользователь аутентифицирован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'isAuthenticated': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Статус аутентификации'
                        ),
                        'user_id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID пользователя'
                        ),
                        'user': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Имя пользователя'
                        ),
                    }
                )
            ),
            401: openapi.Response(
                description="Пользователь не авторизован",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Сообщение об ошибке'
                        )
                    }
                )
            ),
        },
    )
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
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Пользователь уже существует с такими данными'})

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
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password) # если введенные данные есть в базе, то логинем

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

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить профиль пользователя",
        operation_description="Возвращает информацию о профиле пользователя по его ID",
        responses={
            200: ProfileSerializer,
            404: openapi.Response(description="Пользователь не найден"),
        },
    )
    def get(self, request, user_id):
        """
        Получить информацию о профиле пользователя.
        """
        user = User.objects.filter(pk=user_id).first()

        if not user:
            return Response({'detail': 'Пользователь не найден'}, status=404)

        serializer = ProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Обновить дату рождения",
        operation_description="Обновляет дату рождения пользователя. Формат даты: YYYY-MM-DD.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Дата рождения пользователя'),
            },
            required=['birth_date'],
        ),
        responses={
            200: openapi.Response(description="Дата рождения обновлена"),
            400: openapi.Response(description="Неверный формат даты или отсутствует поле"),
            403: openapi.Response(description="Нет доступа к профилю"),
        },
    )
    def post(self, request, user_id):
        """
        Обновить дату рождения пользователя.
        """
        if request.user.id != user_id:
            return Response({'detail': 'Нет доступа к этому профилю'}, status=403)

        birth_date = request.data.get('birth_date')
        if not birth_date:
            return Response({'error': 'Дата рождения обязательна'}, status=400)

        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Неверный формат даты. Ожидается YYYY-MM-DD'}, status=400)

        user = request.user
        user.birth_date = birth_date
        user.save()

        return Response({'message': 'Дата рождения обновлена'}, status=200)

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

    @swagger_auto_schema(
        operation_summary="Получить список пользователей",
        operation_description="Возвращает список всех пользователей.",
        manual_parameters=[
            openapi.Parameter(
                'interests',
                openapi.IN_QUERY,
                description="Список интересов",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'age_min',
                openapi.IN_QUERY,
                description="Минимальный возраст пользователя",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'age_max',
                openapi.IN_QUERY,
                description="Максимальный возраст пользователя",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Список пользователей",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'list_user': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID пользователя"
                                    ),
                                    'username': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Имя пользователя"
                                    ),
                                    'email': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Электронная почта пользователя"
                                    ),
                                    'last_online': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format='date-time',
                                        description="Последний раз онлайн"
                                    ),
                                    'is_online': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description="Пользователь онлайн"
                                    ),
                                    'subscribers_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество подписчиков"
                                    ),
                                    'subscriptions_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество подписок"
                                    ),
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        # Получение параметров фильтра
        interests = request.query_params.getlist('interests', [])  # Список интересов
        age_min = request.query_params.get('age_min')  # Минимальный возраст
        age_max = request.query_params.get('age_max')  # Максимальный возраст

        # Базовый запрос пользователей
        users_query = User.objects.all()

        # Фильтр по интересам
        if interests:
            users_query = users_query.filter(interests__name__in=interests).distinct()

        # Фильтр по возрасту
        today = date.today()
        if age_min:
            birth_date_max = today.replace(year=today.year - int(age_min))  # Дата рождения для минимального возраста
            users_query = users_query.filter(birth_date__lte=birth_date_max)
        if age_max:
            birth_date_min = today.replace(year=today.year - int(age_max))  # Дата рождения для максимального возраста
            users_query = users_query.filter(birth_date__gte=birth_date_min)

        # Сериализация данных
        data = {'list_user': ProfileSerializer(users_query, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Подписка на другого пользователя",
        operation_description="Осуществляет подписку текущего пользователя на других пользователей",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'target_user': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя на, которого осуществляется подписка'),
            },
            required=['target_user'],
        ),
        responses={
            200: openapi.Response(description="Подписка успешно создана"),
            404: openapi.Response(description="Пользователь не найден"),
            409: openapi.Response(description="Подписка уже существует"),
        },
    )
    def post(self, request, user_id):
        current_user = request.user
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=404)

        if Subscription.objects.filter(subscriber=current_user, target=target_user).exists():
            return Response({"status": "Подписка уже существует."})
        
        Subscription.objects.create(subscriber=current_user, target=target_user)
        return Response({"status": "Вы подписались"})

    @swagger_auto_schema(
        operation_summary="Отписка от другого пользователя",
        operation_description="Осуществляет отписку текущего пользователя от других пользователей",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'target_user': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя от которого осуществляется отписка'),
            },
            required=['target_user'],
        ),
        responses={
            200: openapi.Response(description="Подписка успешно удалена"),
            404: openapi.Response(description="Пользователь не найден"),
        },
    )
    def delete(self, request, user_id):
        current_user = request.user
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=404)

        subscription = Subscription.objects.filter(subscriber=current_user, target=target_user)
        if subscription.exists():
            subscription.delete()
            return Response({"status": "Вы отписались"})
        else:
            return Response({"error": "Подписка не существует"}, status=404)

class AddInterestsAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Получить список всех интересов",
        operation_description="Получаем список всех существующих интересов",
        responses={
            200: InterestSerializer,
            404: openapi.Response(description="Интересы не найдены."),
        },
    )
    def get(self, request):
        all_interests = Interests.objects.all()

        data = {'interests': InterestSerializer(all_interests, many=True).data,}

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Добавить интересы для пользователя",
        operation_description="Добавляет интересы для пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'interests_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Список ID интересов"
                ),
            },
            required=['interests_ids'],
        ),
        responses={
            200: openapi.Response(description="Интересы пользователя обновлены"),
            400: openapi.Response(description="Неверные данные"),
            403: openapi.Response(description="Нет доступа к профилю"),
        },
    )
    def post(self, request):
        user = request.user  # Текущий пользователь
        interest_ids = request.data.get('interests_ids', [])  # Список ID интересов

        if not isinstance(interest_ids, list):  # Проверяем, что передан список
            return Response({'error': 'interests_ids must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем интересы из базы данных
        interests = Interests.objects.filter(id__in=interest_ids)

        # Добавляем интересы к пользователю
        user.interests.set(interests)  # Заменяет старые интересы новыми
        user.save()

        return Response({'message': 'Интересы обновлены'}, status=status.HTTP_200_OK)
