import json  # Добавьте этот импорт
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from goods.models import Flower

User = get_user_model()

class CartViewsTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Создаем цветок
        self.flower = Flower.objects.create(name='Rose', price=100)

        # Создаем корзину для пользователя
        self.cart = Cart.objects.create(user=self.user)

    def test_remove_from_cart(self):
        # Добавляем товар в корзину
        CartItem.objects.create(cart=self.cart, flower=self.flower, quantity=1)

        # Проверяем, что товар в корзине
        self.assertEqual(CartItem.objects.count(), 1)

        # Удаляем товар из корзины
        cart_item = CartItem.objects.get(cart=self.cart, flower=self.flower)
        response = self.client.post(reverse('cart:remove_from_cart', args=[cart_item.id]))

        self.assertEqual(response.status_code, 302)  # Проверяем редирект
        self.assertEqual(CartItem.objects.count(), 0)  # Проверяем, что корзина пуста

    def test_cart_view(self):
        # Добавляем товар в корзину
        CartItem.objects.create(cart=self.cart, flower=self.flower, quantity=2)

        response = self.client.get(reverse('cart:cart_view'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Корзина')  # Проверяем, что заголовок присутствует
        self.assertContains(response, self.flower.name)  # Проверяем, что цветок есть в корзине
        self.assertContains(response, 2)  # Проверяем, что количество равно 2