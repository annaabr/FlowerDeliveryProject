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
def confirm_order(request):
    return render(request, 'orders/confirm_order.html', {
        **data,
        'active_page': 'order_form',
    })