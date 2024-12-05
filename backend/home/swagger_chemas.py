from drf_yasg import openapi

# Все видео и видео авторов на которых подписан пользователь
videos_schemas = {
    "operation_summary":"Лента видео",
        "operation_description":"Возвращает ленту видео, включая все видео и видео от подписок.",
        "responses":{
            200: openapi.Response(
                description="Список видео",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'all_videos': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(  # Используем items для массива
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID видео"),
                                        }
                                    ),
                                    'category_video': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID категории видео"),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название категории видео")
                                        }
                                    ),
                                    'video_file': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к видеофайлу"
                                    ),
                                    'author': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID автора"),
                                            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя автора")
                                        }
                                    ),
                                    'author_id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID автора видео"
                                    ),
                                    'views_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество просмотров видео"
                                    ),
                                    'created_at': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        description="Дата и время создания видео (формат: 'YYYY-MM-DD HH:MM')"
                                    ),
                                    'video_preview': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к превью видео"
                                    ),
                                }
                            )
                        ),
                        'subscribed_videos': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(  # Используем items для массива
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID видео"),
                                        }
                                    ),
                                    'category_video': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID категории видео"),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Название категории видео")
                                        }
                                    ),
                                    'video_file': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к видеофайлу"
                                    ),
                                    'author': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID автора"),
                                            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя автора")
                                        }
                                    ),
                                    'author_id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID автора видео"
                                    ),
                                    'views_count': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="Количество просмотров видео"
                                    ),
                                    'created_at': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATETIME,
                                        description="Дата и время создания видео (формат: 'YYYY-MM-DD HH:MM')"
                                    ),
                                    'video_preview': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL или путь к превью видео"
                                    ),
                                }
                            )
                        ),
                    }
                )
            ),
        },
}

# Создание видео
create_video = {
    'operation_summary': "Создать видео",
    'operation_description': "Создает новое видео с указанием категории, файла видео и времени создания.",
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_video': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID категории, к которой относится видео",
            ),
            'video_file': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Путь или URL к видеофайлу",
                example="path_to_video.mp4",
            ),
            'video_preview': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Путь или URL к превью по желанию",
                example="path_to_video.jpg",
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                description="Дата и время создания видео",
                example="2024-12-03 12:00",
            ),
        },
        required=['category_video', 'video_file'],  # Укажите обязательные поля
    ),
    'responses': {
        201: openapi.Response(
            description="Успешное создание видео",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'category_video': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID категории"
                            ),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Название категории"
                            ),
                        },
                        description="Информация о категории"
                    ),
                    'video_file': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Путь или URL к видеофайлу",
                        example="path_to_video.mp4"
                    ),
                    'created_at': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME,
                        description="Дата и время создания видео",
                        example="2024-12-03 12:00"
                    ),
                    'author': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Имя автора видео"
                    ),
                }
            ),
        ),
        400: openapi.Response(
            description="Ошибки валидации",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'errors': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Детализированная информация об ошибках"
                    )
                }
            ),
        ),
    },
}
