from django.db import models
from datetime import date
from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser

class Interests(models.Model):
    name = models.CharField(max_length=128, verbose_name='Интерес')
    image_interest = models.ImageField(upload_to='image/interests', null=True, blank=True, verbose_name='Лого интереса')

    class Meta:
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'

    def __str__(self):
        return f'Интерес - {self.name}'

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(unique=True, max_length=60, verbose_name='Имя пользователя')
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    interests = models.ManyToManyField(Interests, null=True, blank=True, verbose_name='Интересы')
    last_online = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False, editable=False)

    def update_online_status(self):
        """Обновляет статус активности пользователя."""
        if self.last_online and (now() - self.last_online) < timedelta(minutes=5):
            self.is_online = True
        else:
            self.is_online = False
        self.save(update_fields=['is_online'])

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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username} - {self.email}'

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")  # Кто подписывается
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribers")  # На кого подписываются
    created_at = models.DateTimeField(auto_now_add=True)  # Дата подписки

    class Meta:
        unique_together = ('subscriber', 'target')  # Запретить дублирование подписок
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.subscriber.username} -> {self.target.username}"
