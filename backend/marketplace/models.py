from django.db import models

from users.models import User

class AdType(models.Model):
    TYPE = (
        ('rent', 'Аренда',),
        ('sale', 'Продажа',),
    )
    type = models.CharField(default='rent', choices=TYPE, verbose_name='Тип объявления')

    class Meta:
        verbose_name = 'Тип объявления'
        verbose_name_plural = 'Типы объявлений'

    def __str__(self):
        return dict(self.TYPE).get(self.type, 'Неизвестный тип')

class City(models.Model):
    city_name = models.CharField(max_length=64, verbose_name='Имя города')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
    
    def __str__(self):
        return f'{self.city_name}'

class MainCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название главной категории')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главные категории'
    
    def __str__(self):
        return f'{self.name}'
    
class AdditionalCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='Дополнительные категории')
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name='Главная категория')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Дополнительная категория'
        verbose_name_plural = 'Дополнительные категории'
    
    def __str__(self):
        return f'Доп. категория - {self.name} - главная категория {self.main_category.name}'
    
class SubCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='Подкатегории')
    additional_category = models.ForeignKey(AdditionalCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
    
    def __str__(self):
        return f'Подкатегория - {self.name} - доп. категория {self.additional_category.name} - главная категория {self.additional_category.main_category.name}'

class Attribute(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название атрибута')
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name='Главная категория')
    additional_category = models.ForeignKey(AdditionalCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Доп. Категория')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
        verbose_name = 'Главный атрибут'
        verbose_name_plural = 'Главные атрибуты'

    def __str__(self):
        return f'Атрибут: {self.name} - категория: {self.main_category.name}'

class AdditionalAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Атрибут')
    name = models.CharField(max_length=255, verbose_name='Название доп. Атрибута')

    class Meta:
        verbose_name = 'Дополнительный Атрибут'
        verbose_name_plural = 'Дополнительные Атрибуты'

    def __str__(self):
        return f'Доп. Атрибут: {self.name} - Главный атрибут: {self.attribute.name}'

class SubAttribute(models.Model):
    additional_attribute = models.ForeignKey(AdditionalAttribute, on_delete=models.CASCADE, verbose_name='Доп. Атрибут')
    name = models.CharField(max_length=255, verbose_name='Название податрибута')

    class Meta:
        verbose_name = 'Под атрибут'
        verbose_name_plural = 'Под атрибуты'

    def __str__(self):
        return f'Под атрибут {self.name} - Доп. атрибут: {self.additional_attribute.name} - Главный атрибут {self.additional_attribute.attribute.name}'

class RoomCount(models.Model):
    room_count = models.PositiveIntegerField(verbose_name='Количество комнат')

    class Meta:
        verbose_name = 'Количество комнат'
        verbose_name_plural = 'Количества комнат'
    
    def __str__(self):
        return f'Количество комнат -> {self.room_count}'

class Ad(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название предлжения')
    description = models.TextField(verbose_name='Описание предложения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор предложения')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name='Главная категория')
    additional_category = models.ForeignKey(AdditionalCategory, on_delete=models.CASCADE, verbose_name='Доп. категория')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Главный атрибут', related_name='ads_as_attribute')
    additional_attribute = models.ForeignKey(AdditionalAttribute, on_delete=models.CASCADE, verbose_name='Доп. атрибут', related_name='ads_as_additional_attribute')
    subattribute = models.ForeignKey(SubAttribute, on_delete=models.CASCADE, verbose_name='Податрибут атрибут', related_name='ads_as_subattribute')
    ad_type = models.ForeignKey(AdType, on_delete=models.CASCADE, verbose_name='Тип объявления')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
    
    def __str__(self):
        return f'Предложение -> {self.name} - {self.author.username} - {self.main_category.name}'
    
class AdVideo(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='videos',  verbose_name='Предложение')
    video = models.FileField(upload_to='videos/ad_videos/', verbose_name='Видео')

    class Meta:
        verbose_name = 'Видео предложения'
        verbose_name_plural = 'Видео предложений'

    def __str__(self):
        return f'Видео предложения -> {self.ad.name}'

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images', verbose_name='Предложение')
    image = models.ImageField(upload_to='images/ad_images/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото предложения'
        verbose_name_plural = 'Фото предложений'

    def __str__(self):
        return f'Фото предложения -> {self.ad.name}'

class AdAddress(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Предложение')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    street = models.CharField(max_length=64, verbose_name='Улица')
    number = models.CharField(max_length=25, verbose_name='Номер жилья')

    class Meta:
        verbose_name = 'Адрес объявления'
        verbose_name_plural = 'Адреса объвлений'

    def __str__(self):
        return f'Адрес объявления -> {self.ad.name} - {self.city.city_name} - {self.street} - {self.number}'
