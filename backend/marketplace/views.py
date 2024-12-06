from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

from marketplace.models import (
    AdType,
    Ad,
    AdImage,
    AdAddress,
    AdditionalAttribute,
    AdditionalCategory,
    AdVideo,
    Attribute,
    SubAttribute,
    MainCategory,
    SubCategory,
    City,
)

from marketplace.serializers import (
    AdTypeSerializer,
    AdSerializer,
    AdditionalCategorySerializer,
    AdditionalAttributeSerializer,
    AttributeSerializer,
    SubAttributeSerializer,
    SubCategorySerializer,
    MainCategorySerializer,
    AdCreateSerializer,
)

from marketplace.swagger_schemas import (
    detail_main_category_swagger,
    all_main_category,
    detail_additional_category,
    detail_subcategory,
    my_ads_doc,
    create_ad_get,
    create_ad_post,
)

class MainCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**all_main_category)
    def get(self, request):
        main_categories = MainCategory.objects.all()

        data = {'main_categories': MainCategorySerializer(main_categories, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

class DetailMainCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**detail_main_category_swagger)
    def get(self, request, main_category_id):
        try:
            category_main = MainCategory.objects.get(id=main_category_id)
        except MainCategory.DoesNotExist:
            return Response({'message': 'Главная категория не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        # Получение параметров фильтров из запроса
        attribute = request.query_params.get('attribute')
        additional_attribute = request.query_params.get('additional_attribute')
        subattribute = request.query_params.get('subattribute')
        ad_type = request.query_params.get('ad_type')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        # Фильтрация объявлений
        ads_query = Ad.objects.filter(main_category=category_main)

        if attribute:
            ads_query = ads_query.filter(attribute_id=attribute)
        if additional_attribute:
            ads_query = ads_query.filter(additional_attribute_id=additional_attribute)
        if subattribute:
            ads_query = ads_query.filter(subattribute_id=subattribute)
        if ad_type:
            ads_query = ads_query.filter(ad_type_id=ad_type)
        if price_min:
            ads_query = ads_query.filter(price__gte=price_min)
        if price_max:
            ads_query = ads_query.filter(price__lte=price_max)

        # Формирование ответа
        additional_category = AdditionalCategory.objects.filter(main_category=category_main)
        attributes = Attribute.objects.filter(main_category=category_main)
        additional_attributes = AdditionalAttribute.objects.filter(attribute__in=attributes)
        subattributes = SubAttribute.objects.filter(additional_attribute__in=additional_attributes)
        data = {
            'current_category_main': MainCategorySerializer(category_main).data,
            'additional_category': AdditionalCategorySerializer(additional_category, many=True).data,
            'ads': AdSerializer(ads_query, many=True).data,
            'attributes': AttributeSerializer(attributes, many=True).data,
            'additional_attributes': AdditionalAttributeSerializer(additional_attributes, many=True).data,
            'subattributes': SubAttributeSerializer(subattributes, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class DetailAdditionalCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**detail_additional_category)
    def get(self, request, additional_category_id):
        try:
            additional_category = AdditionalCategory.objects.get(id=additional_category_id)
        except AdditionalCategory.DoesNotExist:
            return Response({'message': 'Дополнительная категория не найдена.'}, status=status.HTTP_404_NOT_FOUND)
        
        attribute = request.query_params.get('attribute')
        additional_attribute = request.query_params.get('additional_attribute')
        subattribute = request.query_params.get('subattribute')
        ad_type = request.query_params.get('ad_type')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        # Фильтрация объявлений
        ads_query = Ad.objects.filter(additional_category=additional_category)

        if attribute:
            ads_query = ads_query.filter(attribute_id=attribute)
        if additional_attribute:
            ads_query = ads_query.filter(additional_attribute_id=additional_attribute)
        if subattribute:
            ads_query = ads_query.filter(subattribute_id=subattribute)
        if ad_type:
            ads_query = ads_query.filter(ad_type_id=ad_type)
        if price_min:
            ads_query = ads_query.filter(price__gte=price_min)
        if price_max:
            ads_query = ads_query.filter(price__lte=price_max)

        subcategory = SubCategory.objects.filter(additional_category=additional_category)
        attributes = Attribute.objects.filter(additional_category=additional_category)
        additional_attributes = AdditionalAttribute.objects.filter(attribute__in=attributes)
        subattributes = SubAttribute.objects.filter(additional_attribute__in=additional_attributes)
        data = {
            'current_addtional_category': AdditionalCategorySerializer(additional_category).data,
            'subcategory': SubCategorySerializer(subcategory, many=True).data,
            'ads': AdSerializer(ads_query, many=True).data,
            'attributes': AttributeSerializer(attributes, many=True).data,
            'additional_attributes': AdditionalAttributeSerializer(additional_attributes, many=True).data,
            'subattributes': SubAttributeSerializer(subattributes, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class DetailSubCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**detail_subcategory)
    def get(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return Response({'message': 'Подкатегория не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        attribute = request.query_params.get('attribute')
        additional_attribute = request.query_params.get('additional_attribute')
        subattribute = request.query_params.get('subattribute')
        ad_type = request.query_params.get('ad_type')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        # Фильтрация объявлений
        ads_query = Ad.objects.filter(sub_category=subcategory)

        if attribute:
            ads_query = ads_query.filter(attribute_id=attribute)
        if additional_attribute:
            ads_query = ads_query.filter(additional_attribute_id=additional_attribute)
        if subattribute:
            ads_query = ads_query.filter(subattribute_id=subattribute)
        if ad_type:
            ads_query = ads_query.filter(ad_type_id=ad_type)
        if price_min:
            ads_query = ads_query.filter(price__gte=price_min)
        if price_max:
            ads_query = ads_query.filter(price__lte=price_max)

        attributes = Attribute.objects.filter(subcategory=subcategory)
        additional_attributes = AdditionalAttribute.objects.filter(attribute__in=attributes)
        subattributes = SubAttribute.objects.filter(additional_attribute__in=additional_attributes)
        data = {
            'subcategory': SubCategorySerializer(subcategory).data,
            'ads': AdSerializer(ads_query, many=True).data,
            'attributes': AttributeSerializer(attributes, many=True).data,
            'additional_attributes': AdditionalAttributeSerializer(additional_attributes, many=True).data,
            'subattributes': SubAttributeSerializer(subattributes, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class MyAdsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**my_ads_doc)
    def get(self, request):
        user = request.user

        ads = Ad.objects.filter(author=user)

        data = {'my_ads': AdSerializer(ads, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

class CreateMyAdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**create_ad_get)
    def get(self, request):
        user = request.user

        # Параметры запроса
        main_category_id = request.query_params.get('main_category_id')
        additional_category_id = request.query_params.get('additional_category_id')
        sub_category_id = request.query_params.get('sub_category_id')

        # Результаты
        response_data = {}

        # Главные категории
        if not main_category_id:
            response_data['main_categories'] = MainCategorySerializer(MainCategory.objects.all(), many=True).data

        # Дополнительные категории и атрибуты
        if main_category_id:
            additional_categories = AdditionalCategory.objects.filter(main_category_id=main_category_id)
            attributes = Attribute.objects.filter(main_category_id=main_category_id)

            response_data['additional_categories'] = AdditionalCategorySerializer(additional_categories, many=True).data
            response_data['attributes'] = AttributeSerializer(attributes, many=True).data

        # Подкатегории
        if additional_category_id:
            sub_categories = SubCategory.objects.filter(additional_category_id=additional_category_id)
            additional_attributes = AdditionalAttribute.objects.filter(attribute__main_category_id=main_category_id)

            response_data['sub_categories'] = SubCategorySerializer(sub_categories, many=True).data
            response_data['additional_attributes'] = AdditionalAttributeSerializer(additional_attributes, many=True).data

        # Податрибуты
        if sub_category_id:
            sub_attributes = SubAttribute.objects.filter(additional_attribute__attribute__main_category_id=main_category_id)
            response_data['sub_attributes'] = SubAttributeSerializer(sub_attributes, many=True).data

        return Response(response_data)
    
    @swagger_auto_schema(**create_ad_post)
    def post(self, request):
        user = request.user
        data = request.data

        # Валидируем входящие данные
        serializer = AdCreateSerializer(data=data)
        if serializer.is_valid():
            # Добавляем текущего пользователя как автора
            serializer.validated_data['author'] = user
            ad = serializer.save()  # Создаем объявление

            return Response(
                {"message": "Объявление успешно создано!", "ad": AdSerializer(ad).data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
