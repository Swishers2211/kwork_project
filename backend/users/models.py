from django.db import models
from datetime import date

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(unique=True, max_length=60, verbose_name='Имя пользователя')
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    interests = models.CharField(max_length=255, verbose_name='Интересы', blank=True, null=True)

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year
            # Корректируем возраст, если день рождения еще не наступил в этом году
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None  # Возраст не указан

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username} - {self.email}'
