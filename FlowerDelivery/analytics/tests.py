from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Report
from goods.models import Flower
from orders.models import Order, OrderItem
from django.utils import timezone
from unittest.mock import patch

class ReportViewTests(TestCase):
   def setUp(self):
       # Создаем тестового пользователя
       self.user = User.objects.create_user(username='testuser', password='testpassword')

       # Создаем заказы, указывая пользователя
       self.order1 = Order.objects.create(
           user=self.user,
           status='new',
           created_at=timezone.now(),
           delivery_date=timezone.now() + timezone.timedelta(days=1)
       )
       self.order2 = Order.objects.create(
           user=self.user,
           status='in_progress',
           created_at=timezone.now(),
           delivery_date=timezone.now() + timezone.timedelta(days=1)
       )
       self.order3 = Order.objects.create(user=self.user,
           status='in_delivery',
           created_at=timezone.now(),
           delivery_date=timezone.now() + timezone.timedelta(days=1)
       )
       flower1 = Flower.objects.create(name='Розы', price=6220.0, image='flowers/Pic1.jpg')
       flower2 = Flower.objects.create(name='Гербера крупная', price=1700.0, image='flowers/Pic2.jpg')
       flower3 = Flower.objects.create(name='Гербера', price=3330.0, image='flowers/Pic4.jpg')
       self.order_item1 = OrderItem.objects.create(order=self.order1, flower=flower1, quantity=2)
       self.order_item2 = OrderItem.objects.create(order=self.order2, flower=flower2, quantity=3)
       self.order_item3 = OrderItem.objects.create(order=self.order3, flower=flower3, quantity=1)

   def test_create_daily_report(self):
       response = self.client.get(reverse('create_report'))
       self.assertEqual(response.status_code, 302)  # Проверяем, что происходит редирект

       report = Report.objects.last()
       self.assertIsNotNone(report)
       self.assertEqual(report.orders_count, 3)  # Проверяем, что количество заказов правильно посчитано
       self.assertGreater(report.revenue, 0)  # Проверяем, что выручка больше 0

@patch('analytics.views.bot.send_message')
def test_publish_report(self, mock_send_message):
    report = Report.objects.create(orders_count=1, revenue=100.00)
    response = self.client.get(reverse('publish_report', args=[report.id]))
    self.assertEqual(response.status_code, 302)  # Проверяем, что происходит редирект
    mock_send_message.assert_called_once()  # Проверяем, что сообщение отправлено в Telegram

def test_view_report(self):
    report = Report.objects.create(orders_count=1, revenue=100.00)
    response = self.client.get(reverse('report', args=[report.id]))
    self.assertEqual(response.status_code, 200)  # Проверяем, что страница загружается успешно
    self.assertContains(response, str(report.revenue))  # Проверяем, что выручка отображается на странице