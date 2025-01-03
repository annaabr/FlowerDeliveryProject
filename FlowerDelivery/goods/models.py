from django.db import models
from django.contrib.auth.models import User

class Flower(models.Model):
    name = models.CharField(max_length=100)  # Название
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    image = models.ImageField(upload_to='flowers/')  # Изображение

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name