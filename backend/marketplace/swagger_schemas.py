from drf_yasg import openapi

# Все главные категории
all_main_category = {
    'operation_summary':"Главные категории",
        'operation_description':"Возвращает главные категории, например, недвижимость, транспорт, путешествия и т.п",
        'responses':{
            200: openapi.Response(
                description="Список главных категории",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'main_categories': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID главной категории",
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Название главной категории"
                                    ),
                                }
                            )
                        ),
                    }
                )
            ),
        },
}

# Документация по детальной информации главной категории 
detail_main_category_swagger = {
    'operation_summary':"Выбранная главная категория",
    'operation_description': "Возвращает данные о выбранной главной категории и связанных с ней дополнительных категориях.",
    'manual_parameters': [
        openapi.Parameter(
            'attribute',
            openapi.IN_QUERY,
            description="ID главного атрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'additional_attribute',
            openapi.IN_QUERY,
            description="ID дополнительного атрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'subattribute',
            openapi.IN_QUERY,
            description="ID податрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'ad_type',
            openapi.IN_QUERY,
            description="Тип объявления для фильтрации (например, 'rent' или 'sale')",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'price_min',
            openapi.IN_QUERY,
            description="Минимальная цена для фильтрации",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'price_max',
            openapi.IN_QUERY,
            description="Максимальная цена для фильтрации",
            type=openapi.TYPE_NUMBER
        ),
    ],
    'responses': {
        200: openapi.Response(
            description="Данные о главной категории и связанных дополнительных категориях",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'current_category_main': openapi.Schema(
                        description="Текущая главная категория",
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID главной категории"
                            ),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Название главной категории"
                            ),
                        }
                    ),
                    'additional_category': openapi.Schema(
                        description="Список доп. категорий",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID доп. категории"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название доп. категории"
                                ),
                                'main_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о главной категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID главной категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название главной категории"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'attributes': openapi.Schema(
                        description="Список главных атрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID атрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название атрибута"
                                ),
                                'main_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о главной категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID главной категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название главной категории"
                                        ),
                                    }
                                ),
                                'additional_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о доп. категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID доп. категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название доп. категории"
                                        ),
                                    }
                                ),
                                'subcategory': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о под категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID под категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название под категории"
                                        ),
                                    }
                                ),
                            }
                        )
                    ),
                    'additional_attributes': openapi.Schema(
                        description="Список дополнительных атрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID дополнительного атрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название дополнительного атрибута"
                                ),
                                'attribute': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Связанный главный атрибут",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID атрибута"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название атрибута"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'subattributes': openapi.Schema(
                        description="Список податрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID податрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название податрибута"
                                ),
                                'additional_attribute': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Связанный дополнительный атрибут",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID дополнительного атрибута"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название дополнительного атрибута"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'ads': openapi.Schema(
                        description="Предложения текущей главной категории",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID предложения"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название предложения"
                                ),
                                'description': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Описание предложения"
                                ),
                                'author': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID автора предложения"
                                ),
                                'city': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о городе",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID города"
                                        ),
                                        'city_name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название города"
                                        ),
                                    }
                                ),
                                'ad_type': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Тип объявления",
                                    properties={
                                        'type': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Тип (например, 'rent' или 'sale')"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Человекочитаемое название типа"
                                        ),
                                    }
                                ),
                                'price': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="Цена объявления"
                                ),
                                'videos': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список видео",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL видео"
                                    )
                                ),
                                'images': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список изображений",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL изображения"
                                    )
                                ),
                            }
                        )
                    ),
                }
            )
        ),
        404: openapi.Response(
            description="Главная категория не найдена",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Сообщение об ошибке"
                    )
                }
            )
        ),
    },
}

# Документация по детальной информации доп. категории
detail_additional_category = {
    'operation_summary':"Выбранная доп. категория",
    'operation_description':"Возвращает данные о выбранной доп. категории и связанных с ней дополнительных категориях.",
    'manual_parameters': [
        openapi.Parameter(
            'attribute',
            openapi.IN_QUERY,
            description="ID главного атрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'additional_attribute',
            openapi.IN_QUERY,
            description="ID дополнительного атрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'subattribute',
            openapi.IN_QUERY,
            description="ID податрибута для фильтрации",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'ad_type',
            openapi.IN_QUERY,
            description="Тип объявления для фильтрации (например, 'rent' или 'sale')",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'price_min',
            openapi.IN_QUERY,
            description="Минимальная цена для фильтрации",
            type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'price_max',
            openapi.IN_QUERY,
            description="Максимальная цена для фильтрации",
            type=openapi.TYPE_NUMBER
        ),
    ],
    'responses':{
        200: openapi.Response(
            description="Данные о доп. категории и связанных дополнительных категориях",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'current_addtional_category': openapi.Schema(
                        description="Текущая доплнительная категория",
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID доп. категории"
                            ),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Название доп. категории"
                            ),
                        }
                    ),
                    'subcategory': openapi.Schema(
                        description="Список подкатегорий",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID подкатегории категории"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название подкиатегори категории"
                                ),
                                'additional_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о доп. категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID доп. категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название доп. категории"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'attributes': openapi.Schema(
                        description="Список главных атрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID атрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название атрибута"
                                ),
                                'main_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о главной категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID главной категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название главной категории"
                                        ),
                                    }
                                ),
                                'additional_category': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о доп. категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID доп. категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название доп. категории"
                                        ),
                                    }
                                ),
                                'subcategory': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о под категории",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID под категории"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название под категории"
                                        ),
                                    }
                                ),
                            }
                        )
                    ),
                    'additional_attributes': openapi.Schema(
                        description="Список дополнительных атрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID дополнительного атрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название дополнительного атрибута"
                                ),
                                'attribute': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Связанный главный атрибут",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID атрибута"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название атрибута"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'subattributes': openapi.Schema(
                        description="Список податрибутов",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID податрибута"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название податрибута"
                                ),
                                'additional_attribute': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Связанный дополнительный атрибут",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID дополнительного атрибута"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название дополнительного атрибута"
                                        ),
                                    }
                                )
                            }
                        )
                    ),
                    'ads': openapi.Schema(
                        description="Предложения текущей главной категории",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID предложения"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название предложения"
                                ),
                                'description': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Описание предложения"
                                ),
                                'author': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID автора предложения"
                                ),
                                'city': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о городе",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID города"
                                        ),
                                        'city_name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название города"
                                        ),
                                    }
                                ),
                                'ad_type': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Тип объявления",
                                    properties={
                                        'type': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Тип (например, 'rent' или 'sale')"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Человекочитаемое название типа"
                                        ),
                                    }
                                ),
                                'price': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="Цена объявления"
                                ),
                                'videos': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список видео",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL видео"
                                    )
                                ),
                                'images': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список изображений",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL изображения"
                                    )
                                ),
                            }
                        )
                    ),
                }
            )
        ),
        404: openapi.Response(
            description="Главная категория не найдена",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Сообщение об ошибке"
                    )
                }
            )
        ),
    },
} 

# Документация по странице: текущая подкатегория
detail_subcategory = {
    'operation_summary':"Выбранная подкатегория",
        'operation_description':"Возвращает данные о выбранной подкатегории",
        'manual_parameters': [
            openapi.Parameter(
                'attribute',
                openapi.IN_QUERY,
                description="ID главного атрибута для фильтрации",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'additional_attribute',
                openapi.IN_QUERY,
                description="ID дополнительного атрибута для фильтрации",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'subattribute',
                openapi.IN_QUERY,
                description="ID податрибута для фильтрации",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'ad_type',
                openapi.IN_QUERY,
                description="Тип объявления для фильтрации (например, 'rent' или 'sale')",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'price_min',
                openapi.IN_QUERY,
                description="Минимальная цена для фильтрации",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'price_max',
                openapi.IN_QUERY,
                description="Максимальная цена для фильтрации",
                type=openapi.TYPE_NUMBER
            ),
        ],
        'responses':{
            200: openapi.Response(
                description="Данные о подкатегории",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'subcategory': openapi.Schema(
                            description="Текущая доплнительная подкатегория",
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID подкатегории"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название подкатегории"
                                ),
                            }
                        ),
                        'attributes': openapi.Schema(
                            description="Список главных атрибутов",
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID атрибута"
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Название атрибута"
                                    ),
                                    'main_category': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Информация о главной категории",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID главной категории"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название главной категории"
                                            ),
                                        }
                                    ),
                                    'additional_category': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Информация о доп. категории",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID доп. категории"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название доп. категории"
                                            ),
                                        }
                                    ),
                                    'subcategory': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Информация о под категории",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID под категории"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название под категории"
                                            ),
                                        }
                                    ),
                                }
                            )
                        ),
                        'additional_attributes': openapi.Schema(
                            description="Список дополнительных атрибутов",
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID дополнительного атрибута"
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Название дополнительного атрибута"
                                    ),
                                    'attribute': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Связанный главный атрибут",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID атрибута"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название атрибута"
                                            ),
                                        }
                                    )
                                }
                            )
                        ),
                        'subattributes': openapi.Schema(
                            description="Список податрибутов",
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID податрибута"
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Название податрибута"
                                    ),
                                    'additional_attribute': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Связанный дополнительный атрибут",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID дополнительного атрибута"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название дополнительного атрибута"
                                            ),
                                        }
                                    )
                                }
                            )
                        ),
                        'ads': openapi.Schema(
                            description="Предложения текущей главной категории",
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID предложения"
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Название предложения"
                                    ),
                                    'description': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Описание предложения"
                                    ),
                                    'author': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID автора предложения"
                                    ),
                                    'city': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Информация о городе",
                                        properties={
                                            'id': openapi.Schema(
                                                type=openapi.TYPE_INTEGER,
                                                description="ID города"
                                            ),
                                            'city_name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Название города"
                                            ),
                                        }
                                    ),
                                    'ad_type': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Тип объявления",
                                        properties={
                                            'type': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Тип (например, 'rent' или 'sale')"
                                            ),
                                            'name': openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Человекочитаемое название типа"
                                            ),
                                        }
                                    ),
                                    'price': openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        description="Цена объявления"
                                    ),
                                    'videos': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        description="Список видео",
                                        items=openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="URL видео"
                                        )
                                    ),
                                    'images': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        description="Список изображений",
                                        items=openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="URL изображения"
                                        )
                                    ),
                                }
                            )
                        ),
                    }
                )
            ),
            404: openapi.Response(
                description="Подкатерия не найдена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке"
                        )
                    }
                )
            ),
        },
}

# Документация по старнице: мои объявления
my_ads_doc = {
    'operation_summary':"Мои объявления",
    'operation_description':"Возвращает объявления текущего пользователя",
    'responses':{
        200: openapi.Response(
            description="Данные о выставленных объявлениях текущего пользователя",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'my_ads': openapi.Schema(
                        description="Мои объявления",
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID объявления"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Название объявления"
                                ),
                                'description': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Описание объявления"
                                ),
                                'author': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description="ID автора объявления"
                                ),
                                'city': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Информация о городе",
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description="ID города"
                                        ),
                                        'city_name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Название города"
                                        ),
                                    }
                                ),
                                'ad_type': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Тип объявления",
                                    properties={
                                        'type': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Тип (например, 'rent' или 'sale')"
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="Человеко читаемое название типа"
                                        ),
                                    }
                                ),
                                'price': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="Цена объявления"
                                ),
                                'videos': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список видео",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL видео"
                                    )
                                ),
                                'images': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Список изображений",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="URL изображения"
                                    )
                                ),
                            }
                        )
                    ),
                }
            )
        ),
        404: openapi.Response(
            description="Подкатерия не найдена",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Сообщение об ошибке"
                    )
                }
            )
        ),
    },
}

create_ad_get = {
    'operation_summary':"Получить категории, связанные с объявлением",
    'operation_description':"Возвращает главные, дополнительные, подкатегории, атрибуты и податрибуты, связанные с объявлением, в зависимости от переданных параметров.",
    'manual_parameters':[
        openapi.Parameter(
            'main_category_id',
            openapi.IN_QUERY,
            description="ID главной категории",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'additional_category_id',
            openapi.IN_QUERY,
            description="ID дополнительной категории",
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'sub_category_id',
            openapi.IN_QUERY,
            description="ID подкатегории",
            type=openapi.TYPE_INTEGER
        ),
    ],
    'responses':{
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'main_categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Главные категории",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'additional_categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Дополнительные категории",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'attributes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Атрибуты",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'sub_categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Подкатегории",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'additional_attributes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Дополнительные атрибуты",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
                'sub_attributes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Податрибуты",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)
                ),
            }
        ),
        400: openapi.Response(
            description="Некорректный запрос",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Описание ошибки"
                    )
                }
            )
        ),
    }
}

create_ad_post = {
    'operation_summary':"Создать новое объявление",
        'operation_description':"Создает новое объявление, основываясь на переданных данных.",
        'request_body':openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название объявления"
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Описание объявления"
                ),
                'price': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="Цена объявления"
                ),
                'city_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID города"
                ),
                'ad_type_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID типа объявления"
                ),
                'main_category_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID главной категории"
                ),
                'additional_category_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID дополнительной категории (необязательно)",
                    nullable=True
                ),
                'subcategory_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID подкатегории (необязательно)",
                    nullable=True
                ),
                'attribute_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID атрибута (необязательно)",
                    nullable=True
                ),
                'additional_attribute_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID дополнительного атрибута (необязательно)",
                    nullable=True
                ),
                'subattribute_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID податрибута (необязательно)",
                    nullable=True
                ),
                'videos': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Список видео",
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
                'images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Список изображений",
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
            },
            required=['name', 'description', 'price', 'city_id', 'ad_type_id', 'main_category_id']
        ),
        'responses':{
            201: openapi.Response(
                description="Объявление успешно создано",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение о результате"
                        ),
                        'ad': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Данные созданного объявления"
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации данных",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Ошибки валидации"
                        )
                    }
                )
            ),
        }        
}
