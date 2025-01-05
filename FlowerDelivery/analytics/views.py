from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Report
from orders.models import Order, OrderItem
from goods.models import Flower

from django.conf import settings

data = settings.COMMON_DICT
status_dict = dict(Order.STATUS_CHOICES)


def create_daily_report(request):
    today = timezone.now().date()

    # Получаем заказы за сегодня с статусом 'new'
    new_orders = Order.objects.filter(status='new')
    in_progress_orders = Order.objects.filter(status='in_progress')
    in_delivery_orders = Order.objects.filter(status='in_delivery')
    completed_orders = Order.objects.filter(delivery_date=today, status='completed')

    # Получаем отмененные заказы
    cancelled_orders = Order.objects.filter(delivery_date__lt=today, status__in=['new', 'in_progress', 'in_delivery'])

    # Считаем количество заказов
    orders_count = new_orders.count() + in_progress_orders.count() + in_delivery_orders.count() + cancelled_orders.count()

    # Рассчитываем выручку только для новых заказов, созданных сегодня
    new_orders_created_today = Order.objects.filter(delivery_date=today, status='new')
    revenue = sum(
        item.flower.price * item.quantity
        for order in new_orders_created_today
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
        'revenue': report.revenue,
        'orders_by_status': orders_by_status,
        'active_page': 'report'
    }

    return render(request, 'analytics/report.html', context)