import telebot
from django.conf import settings
from .models import Order

# Создайте экземпляр бота с вашим токеном
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

def send_order_notification(order):
    user = order.user
    flowers_details = '\n'.join([
        f"🌸 {item.flower.name} (кол-во: {item.quantity}, цена: {item.flower.price})"
        for item in order.orderitem_set.all()
    ])

    message = (
        f"🆔 ID заказа: {order.id}\n"
        f"📦 Cтатус заказа: {order.get_status_display()}\n"
        f"👤 Заказчик: {user.username} (ID: {user.id})\n"
        f"💐 Букеты:\n{flowers_details}\n"
        f"📅 Дата доставки: {order.delivery_date}\n"
        f"🕒 Время доставки: {order.delivery_time_interval}\n"
        f"🏠 Адрес доставки: {order.address}\n"
        f"📝 Комментарий: {order.customer_comment}\n"
    )

    chat_id = settings.TELEGRAM_CHAT_ID
    bot.send_message(chat_id, message)

def send_order_status_update(order):
    status_display = order.get_status_display()
    message = (
        f"🆔 ID заказа: {order.id}\n"
        f"📦 Новый статус: {status_display}\n"
    )

    chat_id = settings.TELEGRAM_CHAT_ID
    bot.send_message(chat_id, message)