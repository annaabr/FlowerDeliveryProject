from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from goods.models import Flower
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import telebot
from django.http import JsonResponse
import json

from django.conf import settings

data = settings.COMMON_DICT

@login_required
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Добавляем товар в корзину или обновляем количество
    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)

    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        cart_item.quantity = int(quantity)
        cart_item.save()
        return JsonResponse({'success': True})

    if not created:  # Если товар уже есть в корзине, увеличиваем количество
        cart_item.quantity += 1
        cart_item.save()

    return redirect('goods:flower_catalog')

@login_required
def remove_from_cart(request, cart_item_id):
    cart = get_object_or_404(Cart, user=request.user)

    # Получаем элемент с соответствующим cart_item_id и удаляем его
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

    # Удаляем найденный товар
    cart_item.delete()

    return redirect('cart:cart_view')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Обрабатываем обновление количества товара
        for item in CartItem.objects.filter(cart=cart):
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('cart:cart_view')

    # Получаем обновленный список товаров в корзине
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/cart_view.html', {**data, 'items': items})
