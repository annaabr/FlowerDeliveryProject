from django.db import models
from django.contrib.auth.models import User
from goods.models import Flower
from django.utils import timezone
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('in_delivery', 'В доставке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Не выполнен в срок'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower, through='OrderItem')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    address = models.TextField()  # Адрес доставки
    delivery_date = models.DateField(null=False, blank=False)  # Дата доставки
    delivery_time_interval = models.CharField(
        max_length=20,
        choices=[(interval, interval) for interval in settings.COMMON_DICT['delivery_time_intervals']],
        null=False,
        blank=False
    )  # Временной интервал доставки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания заказа
    customer_comment = models.CharField(max_length=250, blank=True)  # Комментарий пользователя

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)