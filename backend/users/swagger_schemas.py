from drf_yasg import openapi

list_user_schemas = {
    "operation_summary": "Получить список пользователей",
    "operation_description": "Возвращает список всех пользователей.",
    "manual_parameters": [
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
    "responses": {
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
                                'user_videos': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Публикации пользователя",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID видео"
                                            ),
                                            'category_video': openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'name': openapi.Schema(
                                                        type=openapi.TYPE_STRING,
                                                        description="Категория видео"
                                                    )
                                                }
                                            ),
                                            'video_file': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Путь к видеофайлу"
                                            ),
                                            'author': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Автор видео"
                                            ),
                                            'author_id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID автора видео"
                                            ),
                                            'views_count': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="Количество просмотров"
                                            ),
                                            'created_at': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                format='date-time',
                                                description="Дата создания"
                                            ),
                                            'video_preview': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Превью видео"
                                            )
                                        }
                                    )
                                )
                            }
                        )
                    )
                }
            )
        )
    }
}


# User profile
user_profile_schemas = {
    "operation_summary":"Получить профиль пользователя",
        "operation_description":"Возвращает информацию о профиле пользователя по его ID",
        "responses":{
            200: openapi.Schema(
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
                    'user_videos': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="Публикации пользователя",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID видео"
                                ),
                                'category_video': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Категория видео"
                                        )
                                    }
                                ),
                                'video_file': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Путь к видеофайлу"
                                ),
                                'author': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Автор видео"
                                ),
                                'author_id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID автора видео"
                                ),
                                'views_count': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="Количество просмотров"
                                ),
                                'created_at': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format='date-time',
                                    description="Дата создания"
                                ),
                                'video_preview': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Превью видео"
                                )
                            }
                        )
                    )
                }
            ),
            404: openapi.Response(description="Пользователь не найден"),
        },
}