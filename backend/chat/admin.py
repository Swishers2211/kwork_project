from django.contrib import admin
from django.utils.html import format_html
from chat.models import Room, Message, VoiceMessage

# Зарегистрируем модель VoiceMessage
admin.site.register(VoiceMessage)

class CombinedMessageInline(admin.TabularInline):
    # Определяем, что этот Inline будет работать с двумя моделями: Message и VoiceMessage
    model = Message
    fields = ['id', 'sender', 'message_text', 'created_at', 'message_read', 'message_type', 'message_link']
    extra = 0  # Не добавлять пустые строки для создания новых записей
    readonly_fields = ['id', 'sender', 'message_text', 'created_at', 'message_read', 'message_type', 'message_link']  # Только для чтения
    
    def message_type(self, obj):
        if isinstance(obj, VoiceMessage):
            return "Голосовое сообщение"
        return "Текстовое сообщение"
    message_type.short_description = "Тип сообщения"

    def message_link(self, obj):
        if isinstance(obj, VoiceMessage):
            return format_html('<a href="{}" target="_blank">Прослушать</a>', obj.voice_message.url)
        return None  # Для текстовых сообщений не показываем ссылку
    message_link.short_description = "Ссылка на голосовое сообщение"

    def has_add_permission(self, request, obj=None):
        return False  # Не разрешать добавление новых сообщений через админку

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'sender', 'message_text', 'created_at', 'message_read']
    list_filter = ['room', 'created_at']  # Добавляем фильтр по комнате и дате
    search_fields = ['message_text', 'sender__username']  # Поиск по тексту сообщения и имени отправителя

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'message_count', 'view_messages_link']
    inlines = [CombinedMessageInline]  # Добавляем только один inline для сообщений (включая текстовые и голосовые)

    def message_count(self, obj):
        # Подсчитываем все сообщения (текстовые + голосовые)
        text_messages_count = obj.message_set.count()
        voice_messages_count = obj.voicemessage_set.count()
        return text_messages_count + voice_messages_count
    message_count.short_description = "Количество сообщений"

    def view_messages_link(self, obj):
        # Фильтр по текстовым и голосовым сообщениям (вместе)
        url = f"/api/admin/chat/message/?room__id__exact={obj.id}"
        return format_html(f'<a href="{url}">Посмотреть все сообщения</a>')
    view_messages_link.short_description = "Все сообщения"
