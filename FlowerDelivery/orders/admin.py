from django.contrib import admin
from .models import Order
from .bot import send_order_status_update

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'delivery_date', 'created_at')

    def save_model(self, request, obj, form, change):
        # Сохраняем объект заказа
        super().save_model(request, obj, form, change)

        # Если это изменение существующего заказа, отправляем уведомление
        if change:
            send_order_status_update(obj)

# Регистрируем модель и класс администратора
admin.site.register(Order, OrderAdmin)