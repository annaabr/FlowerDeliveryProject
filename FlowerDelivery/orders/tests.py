from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from goods.models import Flower
from cart.models import Cart, CartItem

class OrderViewTests(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем корзину для пользователя
        self.cart = Cart.objects.create(user=self.user)

    def test_order_review_empty_cart(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders:order_review'))
        self.assertRedirects(response, reverse('cart:cart_view'))

    def test_order_review_with_items(self):
        self.client.login(username='testuser', password='testpassword')
        flower = Flower.objects.create(name='Розы', price=6220.0, image='flowers/Pic1.jpg')
        CartItem.objects.create(cart=self.cart, flower=flower, quantity=2)

        response = self.client.get(reverse('orders:order_review'))
        self.assertEqual(response.status_code, 200)

    def test_order_form_empty_cart_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders:order_form', args=(0,)))
        self.assertRedirects(response, reverse('cart:cart_view'))


    def test_order_history(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 200)
