from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages

from django.conf import settings

data = settings.COMMON_DICT

@login_required
def order_review(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.flower.price * item.quantity for item in cart_items)

    return render(request, 'orders/order_review.html', {
        **data,
        'active_page': 'order_review',
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)  # Уберите request.user
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Получаем номер телефона из формы
            contact_phone = form.cleaned_data.get('phone')
            # Добавляем номер телефона в начало комментария, если он есть
            if contact_phone:
                order.customer_comment = f"Телефон заказчика: {contact_phone}\n{order.customer_comment or ''}"

            order.save()

            # Сохранение товаров в заказе
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                OrderItem.objects.create(order=order, flower=item.flower, quantity=item.quantity)

            # Очищаем корзину
            cart_items.delete()

            messages.success(request, 'Заказ успешно оформлен.')
            return redirect('goods:flower_catalog')
    else:
        form = OrderForm()  # Уберите request.user

    # Вычисляем дату доставки
    today = datetime.now().date()
    min_delivery_date = (today + timedelta(days=1)).isoformat()

    return render(request, 'orders/order_form.html', {
        **data,
        'active_page': 'order_form',
        'form': form,
        'min_delivery_date': min_delivery_date,  # Передаем минимальную дату
    })


    # Вычисляем дату доставки
    today = datetime.now().date()
    min_delivery_date = (today + timedelta(days=1)).isoformat()

    return render(request, 'orders/order_form.html', {
        **data,
        'active_page': 'order_form',
        'form': form,
        'min_delivery_date': min_delivery_date,  # Передаем минимальную дату
    })



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Добавляем общую стоимость для каждого заказа
    for order in orders:
        order.total_price = sum(item.flower.price * item.quantity for item in order.orderitem_set.all())

    return render(request, 'orders/order_history.html', {**data, 'orders': orders, 'active_page': 'order_history'})

@login_required
def repeat_order(request, order_id):
    original_order = Order.objects.get(id=order_id, user=request.user)


    # Создание нового заказа на основе оригинального
    new_order = Order.objects.create(
        user=request.user,
        address=original_order.address,
        delivery_date=original_order.delivery_date,
        delivery_time_interval=original_order.delivery_time_interval,
        customer_comment=original_order.customer_comment,
        status='new'
    )

#    for item in original_order.orderitem_set.all():
#        new_item = OrderItem.objects.create(order=new_order, flower=item.flower, quantity=item.quantity)
#        print(f"Created new OrderItem: {new_item} for order {new_order.id}")

    for item in original_order.orderitem_set.all():
        OrderItem.objects.create(order=new_order, flower=item.flower, quantity=item.quantity)

    return redirect('orders:order_form')