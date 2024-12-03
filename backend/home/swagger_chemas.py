from drf_yasg import openapi

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
