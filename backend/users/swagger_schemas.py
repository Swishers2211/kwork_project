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
                    'follow_you': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Следует за вами"
                    ),
                    'follow_him': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Следуете за ним"
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

status_subscribe = {
    "operation_summary": "Статус подписки",
    "operation_description": "Возвращает статус подписки",
    "manual_parameters": [
        openapi.Parameter(
            'target_user',
            openapi.IN_QUERY,
            description="ID пользователя",
            type=openapi.TYPE_STRING
        ),
    ],
    "responses": {
        200: openapi.Response(
            description="Статус подписки",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Статус подписки",
                    )
                }
            )
        )
    }
}

# Отправка запроса в друзья
send_friend_request_schemas = {
    'operation_summary': "Отправить запрос в друзья",
    'operation_description': "Отправляет запрос на добавление в друзья указанному пользователю по его `user_id`.",
    'responses': {
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID запроса дружбы'),
                'sender': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID отправителя'),
                'sender_username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя отправителя'),
                'receiver': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID получателя'),
                'receiver_username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя получателя'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Статус запроса дружбы', enum=['pending', 'accepted', 'declined']),
                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Дата и время создания'),
                'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Дата и время последнего обновления'),
            }
        ),
        400: openapi.Response(description="Запрос уже отправлен"),
        404: openapi.Response(description="Пользователь не найден"),
    },
}

# Ответить на запрос в друзья
respond_to_friend_request = {
        "request_body":openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Действие: `accept` для принятия или `decline` для отклонения.",
                    enum=['accept', 'decline'],
                ),
            },
            required=['action'],
        ),
        "responses":{
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID запроса дружбы'),
                    'sender': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID отправителя'),
                    'sender_username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя отправителя'),
                    'receiver': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID получателя'),
                    'receiver_username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя получателя'),
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Статус запроса дружбы',
                        enum=['pending', 'accepted', 'declined'],
                    ),
                    'created_at': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME,
                        description='Дата и время создания запроса',
                    ),
                    'updated_at': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME,
                        description='Дата и время последнего обновления запроса',
                    ),
                },
            ),
            400: openapi.Response(description="Неверное действие"),
            404: openapi.Response(description="Запрос не найден"),
        },
        "operation_summary":"Ответ на запрос дружбы",
        "operation_description":"Позволяет пользователю принять или отклонить запрос дружбы, передав действие в теле запроса.",
}

# Список друзей
friend_list_schema = {
    "operation_summary": "Список друзей",
    "operation_description": "Возвращает список всех друзей текущего пользователя. Показывает друзей, у которых статус запроса дружбы — `accepted`.",
    "responses": {
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID друга'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя друга'),
                },
            ),
            description="Список друзей пользователя",
        ),
    },
}
