from rest_framework import serializers

from marketplace.models import (
    MainCategory,
    AdditionalCategory,
    SubCategory,
    Attribute,
    AdditionalAttribute,
    SubAttribute, 
    City,
    RoomCount,
    Ad,
    AdImage,
    AdVideo,
    AdAddress,
    AdType
)

class AdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdType
        fields = ['type']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name']

class AdditionalCategorySerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer()

    class Meta:
        model = AdditionalCategory
        fields = ['id', 'name', 'main_category']

class SubCategorySerializer(serializers.ModelSerializer):
    additional_category = AdditionalCategorySerializer()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'additional_category']

class AttributeSerializer(serializers.ModelSerializer):
    additional_category = AdditionalCategorySerializer()
    main_category = MainCategorySerializer()
    subcategory = SubCategorySerializer()

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'main_category', 'additional_category', 'subcategory']

class AdditionalAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = AdditionalAttribute
        fields = ['id', 'name', 'attribute']

class SubAttributeSerializer(serializers.ModelSerializer):
    additional_attribute = AdditionalAttributeSerializer()

    class Meta:
        model = SubAttribute
        fields = ['id', 'name', 'additional_attribute']

class AdVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdVideo
        fields = ['id', 'ad', 'video']

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'ad', 'image']


class AdSerializer(serializers.ModelSerializer):
    ad_type = AdTypeSerializer()
    city = CitySerializer()
    videos = AdVideoSerializer(source='videos', many=True, read_only=True)
    images = AdImageSerializer(source='images', many=True, read_only=True)
    main_category = MainCategorySerializer()
    additional_category = AdditionalCategorySerializer()
    subcategory = SubCategorySerializer()
    attribute = AttributeSerializer()
    additional_attribute = AdditionalAttributeSerializer()
    subattribute = SubAttributeSerializer()

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'description', 'author', 'city', 'ad_type', 
            'price', 'videos', 'images', 'created_at', 'main_category', 
            'additional_category', 'subcategory', 'attribute', 
            'additional_attribute', 'subattribute'
        ]

class AdCreateSerializer(serializers.ModelSerializer):
    ad_type = AdTypeSerializer()
    city = CitySerializer()

    # Видео и изображения через связанные объекты
    videos = AdVideoSerializer(source='videos', many=True, read_only=False)
    images = AdImageSerializer(source='images', many=True, read_only=False)

    main_category = MainCategorySerializer()
    additional_category = AdditionalCategorySerializer()
    subcategory = SubCategorySerializer()
    attribute = AttributeSerializer()
    additional_attribute = AdditionalAttributeSerializer()
    subattribute = SubAttributeSerializer()

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'description', 'author', 'city', 'ad_type', 
            'price', 'videos', 'images', 'created_at', 
            'main_category', 'additional_category', 'subcategory', 
            'attribute', 'additional_attribute', 'subattribute'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        videos_data = validated_data.pop('videos', [])
        images_data = validated_data.pop('images', [])

        ad = Ad.objects.create(**validated_data)

        # Создание связанных видео
        for video_data in videos_data:
            AdVideo.objects.create(ad=ad, **video_data)

        # Создание связанных изображений
        for image_data in images_data:
            AdImage.objects.create(ad=ad, **image_data)

        return ad
