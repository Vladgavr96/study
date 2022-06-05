from django.db import models

class Tag(models.Model):
    name = models.CharField(verbose_name="имя тега", max_length=254, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)