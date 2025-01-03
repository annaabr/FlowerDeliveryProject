from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()

    class Meta:
        verbose_name = 'Зарегистрированный пользователь'
        verbose_name_plural = 'Зарегистрированные пользователи'

    def __str__(self):
        return self.user.username