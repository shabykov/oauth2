from django.db import models

from ..core.models import User
from oauth2_provider.models import Application


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    applications = models.ManyToManyField(
        Application,
        verbose_name='Приложения'
    )

    def __str__(self):
        if self.user:
            return self.user.username

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
