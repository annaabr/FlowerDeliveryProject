from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Report
from orders.models import Order, OrderItem
from goods.models import Flower
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
import telebot

from django.conf import settings

data = settings.COMMON_DICT
status_dict = dict(Order.STATUS_CHOICES)

# Создаем клиента для Telegram
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

def publish_report(request, report_id):
    report = Report.objects.get(id=report_id)

    # Форматируем дату и время
    date_str = report.created_at.strftime('%d.%m.%Y')
    time_str = report.created_at.strftime('%H.%M')

    # Получаем количество заказов по статусам
    new_orders_count = len(report.orders_list_new.split(',')) if report.orders_list_new.strip() else 0
    in_progress_count = len(report.orders_list_in_progress.split(',')) if report.orders_list_in_progress.strip() else 0
    in_delivery_count = len(report.orders_list_in_delivery.split(',')) if report.orders_list_in_delivery.strip() else 0
    completed_count = len(report.orders_list_completed.split(',')) if report.orders_list_completed.strip() else 0
    cancelled_count = len(report.orders_list_cancelled.split(',')) if report.orders_list_cancelled.strip() else 0

    # Формируем сообщение для отправки
    message = (
        f"Отчет (ID: {report.id})\n"
        f"Дата: {date_str}\n"
        f"Время: {time_str}\n\n"
        f"Выручка: {report.revenue} руб.\n\n"
        f"Количество активных заказов: {report.orders_count}\n\n"
        f"Распределение по статусам:\n"
        f"Новые: {new_orders_count}\n"
        f"В работе: {in_progress_count}\n"
        f"В доставке: {in_delivery_count}\n"
        f"Завершены: {completed_count}\n"
        f"Не выполнены в срок: {cancelled_count}\n"
    )

    # Отправляем сообщение в Telegram
    chat_id = settings.TELEGRAM_CHAT_ID
    bot.send_message(chat_id=chat_id, text=message)

    messages.success(request, 'Отчет успешно отправлен')

    # Перенаправляем обратно на страницу отчета с сообщением
    return redirect('report', report_id=report.id)  # Перенаправляем на страницу отчета

def create_daily_report(request):
    today = timezone.now().date()

    # Получаем заказы за сегодня с статусами 'new', 'in_progress', 'in_delivery'
    new_orders = Order.objects.filter(created_at__date=today, status='new')
    in_progress_orders = Order.objects.filter(created_at__date=today, status='in_progress')
    in_delivery_orders = Order.objects.filter(created_at__date=today, status='in_delivery')
    completed_orders = Order.objects.filter(delivery_date=today, status='completed')

    # Получаем отмененные заказы
    cancelled_orders = Order.objects.filter(delivery_date__lt=today, status__in=['new', 'in_progress', 'in_delivery'])

    # Считаем количество заказов
    orders_count = new_orders.count() + in_progress_orders.count() + in_delivery_orders.count() + cancelled_orders.count()

    # Рассчитываем выручку для заказов со статусами 'new', 'in_progress', 'in_delivery', созданных сегодня
    active_orders = Order.objects.filter(created_at__date=today, status__in=['new', 'in_progress', 'in_delivery'])
    revenue = sum(
        item.flower.price * item.quantity
        for order in active_orders
        for item in order.orderitem_set.all()
    )

    # Создаем новый отчет
    report = Report.objects.create(
        orders_count=orders_count,
        revenue=revenue,
        orders_list_new=','.join(map(str, new_orders.values_list('id', flat=True))),
        orders_list_in_progress=','.join(map(str, in_progress_orders.values_list('id', flat=True))),
        orders_list_in_delivery=','.join(map(str, in_delivery_orders.values_list('id', flat=True))),
        orders_list_completed=','.join(map(str, completed_orders.values_list('id', flat=True))),
        orders_list_cancelled=','.join(map(str, cancelled_orders.values_list('id', flat=True))),
    )

    # Перенаправляем на страницу отчета с передачей данных
    return redirect('report', report_id=report.id)

def view_report(request, report_id):
    report = Report.objects.get(id=report_id)

    # Получаем сообщение из GET-параметров
    message = request.GET.get('message')

    # Подготовка данных для контекста
    orders_by_status = {
        'new': report.orders_list_new.split(',') if report.orders_list_new.strip() else [],
        'in_progress': report.orders_list_in_progress.split(',') if report.orders_list_in_progress.strip() else [],
        'in_delivery': report.orders_list_in_delivery.split(',') if report.orders_list_in_delivery.strip() else [],
        'completed': report.orders_list_completed.split(',') if report.orders_list_completed.strip() else [],
        'cancelled': report.orders_list_cancelled.split(',') if report.orders_list_cancelled.strip() else []
    }

    context = {
        **data,
        'report': report,
        'status_dict': status_dict,
        'orders_count': report.orders_count,
        'message': message,
        'revenue': report.revenue,
        'orders_by_status': orders_by_status,
        'active_page': 'report'
    }

    return render(request, 'analytics/report.html', context)
