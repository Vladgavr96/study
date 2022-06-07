from datetime import datetime

from django.db import models
from django.http import HttpRequest
from django.utils import timezone

from user.models import User


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Имя альбома', null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Дата изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name='Пользователь',
                             null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ("user", "name",)
        unique_together = ('name', 'user')


