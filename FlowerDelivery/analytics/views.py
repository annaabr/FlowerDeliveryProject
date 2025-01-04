from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from orders.models import Order
from django.utils import timezone
from collections import defaultdict
from django.conf import settings

data = settings.COMMON_DICT
status_dict = dict(Order.STATUS_CHOICES)


@staff_member_required
def generate_report(request):
    today = timezone.now().date()
    previous_reports = Report.objects.filter(created_at__date=today)

    if previous_reports.exists():
        previous_report = previous_reports.last()
        previous_orders = previous_report.orders_list_new.split(',')  # Список заказов из предыдущего отчета
        previous_orders = set(previous_orders)  # Для быстрого поиска
    else:
        previous_orders = set()

    current_orders = Order.objects.filter(created_at__date=today).exclude(status__in=['completed', 'cancelled'])
    current_orders_ids = set(current_orders.values_list('id', flat=True))

    revenue = 0
    orders_count = len(current_orders)
    orders_by_status = defaultdict(list)

    for order in current_orders:
        order_items = order.orderitem_set.all()
        for item in order_items:
            flower = item.flower
            revenue += flower.price * item.quantity

        orders_by_status[order.status].append(order.id)

    # Подготовка списков заказов по статусам
    orders_list_new = ','.join(map(str, orders_by_status['new']))
    orders_list_in_progress = ','.join(map(str, orders_by_status['in_progress']))
    orders_list_in_delivery = ','.join(map(str, orders_by_status['in_delivery']))
    orders_list_completed = ','.join(map(str, orders_by_status['completed']))
    orders_list_cancelled = ','.join(map(str, orders_by_status['cancelled']))


    # Включаем заказы из предыдущего отчета, если они были изменены
    for order_id in previous_orders:
        if order_id in current_orders_ids:
            continue  # Пропускаем, если заказ уже есть в текущих заказах

        order = Order.objects.get(id=order_id)
    if order.status not in ['completed', 'cancelled']:
        orders_by_status[order.status].append(order.id)

    # Создаем отчет
    report = Report.objects.create(
        orders_count=orders_count,
        revenue=revenue,
        orders_list_new=orders_list_new,
        orders_list_in_progress=orders_list_in_progress,
        orders_list_in_delivery=orders_list_in_delivery,
        orders_list_completed=orders_list_completed,
        orders_list_cancelled=orders_list_cancelled,
    )

    # Перенаправление на страницу отчета
    return redirect('report_detail', report_id=report.id)

@staff_member_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    # Создаем словарь для хранения заказов по статусам
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
        'orders_by_status': orders_by_status,
        'status_dict': status_dict,
        'active_page': 'report_detail'
    }

    return render(request, 'analytics/report_detail.html', context)