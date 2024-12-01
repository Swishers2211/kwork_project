from django.contrib import admin
from marketplace.models import (
    AdType,
    City,
    AdAddress,
    Ad,
    AdVideo,
    AdImage,
    RoomCount,
    Attribute,
    AdditionalAttribute,
    AdditionalCategory,
    MainCategory,
    SubCategory,
    SubAttribute
)

# Регистрация моделей
admin.site.register(AdType)
admin.site.register(City)
admin.site.register(RoomCount)
admin.site.register(SubCategory)
admin.site.register(AdditionalAttribute)
admin.site.register(SubAttribute)

# Inline для изображений
class AdImageInline(admin.TabularInline):
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
    get_city.short_description = 'City'

# Inline для дополнительных категорий
class AdditionalCategoryInline(admin.TabularInline):  # Табличный вывод
    model = AdditionalCategory
    extra = 1  # Количество пустых строк для добавления новых объектов

# Inline для атрибутов
class AttributeInline(admin.TabularInline):  # Табличный вывод
    model = Attribute
    extra = 1  # Количество пустых строк для добавления новых объектов

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [AdditionalCategoryInline, AttributeInline]

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(AdditionalCategory)
class AdditionalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [SubCategoryInline]

class AttributeInline(admin.TabularInline):
    model = AdditionalAttribute
    extra = 1

@admin.register(Attribute)
class AdAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [AttributeInline]
