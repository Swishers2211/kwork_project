from django.db import models

from users.models import User

class Room(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='Получатель')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        unique_together = ('sender', 'receiver')
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.sender.username} - {self.receiver.username}'
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Чат')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender', verbose_name='Отправитель')
    message_text = models.TextField(verbose_name='Текст сообщения', blank=True, null=True)
    message_image = models.ImageField(upload_to='messages/images/', blank=True, null=True, verbose_name='Изображение')
    message_video = models.FileField(upload_to='messages/videos/', blank=True, null=True, verbose_name='Видеофайл')
    message_read = models.BooleanField(default=False, verbose_name='Сообщение прочитано (Не прочитано по умолчанию)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = [
            models.Index(fields=['room', 'created_at']),
        ]

    def __str__(self):
        sender = self.sender.username
        # Определяем получателя: если отправитель не является отправителем комнаты, значит он получатель
        if self.sender == self.room.sender:
            receiver = self.room.receiver.username
        else:
            receiver = self.room.sender.username
        return f'Чат: #{self.room.id} - Отправитель: {sender} - Получатель: {receiver} - Сообщение: {self.message_text}'

class VoiceMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель голосового сообщения')
    voice_message = models.FileField(upload_to='messages/voice_messages/')
    message_read = models.BooleanField(default=False, verbose_name='Сообщение голосовое прочитано (Не прочитано по умолчанию)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки голового сообщения')

    class Meta:
        verbose_name = 'Голосовое сообщение'
        verbose_name_plural = 'Голосовые сообщения'

    def __str__(self):
        sender = self.sender.username
        # Определяем получателя: если отправитель не является отправителем комнаты, значит он получатель
        if self.sender == self.room.sender:
            receiver = self.room.receiver.username
        else:
            receiver = self.room.sender.username
        return f'Чат: #{self.room.id} - Отправитель: {sender} - Получатель: {receiver} - Сообщение: {self.voice_message}'
