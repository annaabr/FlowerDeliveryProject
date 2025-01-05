from django.db import models
from django.utils import timezone
from orders.models import Order

class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания отчета
    orders_count = models.PositiveIntegerField()  # Количество заказов
    revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Выручка за день
    orders_list_new = models.TextField(default='')  # Список ID новых заказов
    orders_list_in_progress = models.TextField(default='')  # Список ID заказов в работе
    orders_list_in_delivery = models.TextField(default='')  # Список ID заказов в доставке
    orders_list_completed = models.TextField(default='')  # Список ID выполненных заказов
    orders_list_cancelled = models.TextField(default='')  # Список ID отмененных заказов

    def __str__(self):
        return f"Отчет от {self.created_at}"