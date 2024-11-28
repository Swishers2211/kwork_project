from django.contrib import admin
from marketplace.models import (
    AdType,
    City,
    AdAddress,
    Ad,
    AdVideo,
    AdImage,
    RoomCount,
    AdAttribute,
    AdAttributeValue,
    AdditionalCategory,
    MainCategory,
    SubCategory
)

admin.site.register(AdType)
admin.site.register(City)
admin.site.register(AdAddress)
admin.site.register(RoomCount)
admin.site.register(AdditionalCategory)
admin.site.register(AdAttribute)
admin.site.register(AdAttributeValue)
admin.site.register(MainCategory)
admin.site.register(SubCategory)

# Inline для картинок
class AdImageInline(admin.TabularInline):  # Используем TabularInline для табличного отображения
    model = AdImage
    extra = 1  # Количество пустых строк для добавления новых объектов

# Inline для видео
class AdVideoInline(admin.TabularInline):
    model = AdVideo
    extra = 1

# Inline для адресов
class AdAddressInline(admin.TabularInline):
    model = AdAddress
    extra = 1

# Кастомизация админки для Ad
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'author', 'get_city', 'ad_type', 'created_at')  # Поля для отображения в списке объектов
    list_filter = ('ad_type', 'created_at')  # Фильтры в боковой панели
    search_fields = ('name', 'description')  # Поля для поиска
    inlines = [AdImageInline, AdVideoInline, AdAddressInline]  # Подключение инлайнов

    def get_city(self, obj):
        address = obj.adaddress_set.first() 
        return address.city.city_name if address and address.city else "—"
    get_city.short_description = 'сity'
