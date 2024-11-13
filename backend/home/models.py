from django.db import models

from users.models import User

class CategoryVideo(models.Model):
    name = models.CharField(max_length=70, verbose_name='Категория видео')

    class Meta:
        verbose_name = 'Категория видео'
        verbose_name_plural = 'Категории видео'

    def __str__(self):
        return f'Категория {self.name}'

class Video(models.Model):
    category_video = models.ForeignKey(CategoryVideo, on_delete=models.CASCADE, verbose_name='Категория видео')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор видео')
    video_file = models.FileField(upload_to='videos/', verbose_name='Видео файл')
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'Видео - {self.video_file}, просмотры - {self.views_count}, опубликовано - {self.created_at}'

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', verbose_name='Видео')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(max_length=1000, verbose_name='Содержание комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.video.video_file}'
