# Тестируем, что функция `catalog` возвращает корректный контекст
# и рендерит правильный шаблон

from django.test import TestCase
from django.urls import reverse
from .models import Flower
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class CatalogViewTests(TestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Создание нескольких объектов Flower

        self.flower1 = Flower.objects.create(name='Белые розы', price=6220.0, image='flowers/Pic6.jpg')
        self.flower2 = Flower.objects.create(name='Хризантемы', price=3330.0, image='flowers/Pic5.jpg')
        self.flower3 = Flower.objects.create(name='Гербера', price=3330.0, image='flowers/Pic4.jpg')
        self.flower4 = Flower.objects.create(name='Хризантемы пастель', price=3730.0, image='flowers/Pic3.jpg')
        self.flower5 = Flower.objects.create(name='Гербера крупная', price=1700.0, image='flowers/Pic2.jpg')
        self.flower6 = Flower.objects.create(name='Розы', price=6220.0, image='flowers/Pic1.jpg')

    def test_catalog_view_status_code(self):
        response = self.client.get(reverse('goods:flower_catalog'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_view_template_used(self):
        response = self.client.get(reverse('goods:flower_catalog'))
        self.assertTemplateUsed(response, 'main/catalog.html')

    def test_catalog_view_context(self):
        response = self.client.get(reverse('goods:flower_catalog'))
        self.assertIn('flowers', response.context)
        self.assertEqual(len(response.context['flowers']), 6)  # Проверяем, что в контексте 6 букетов

    def test_catalog_view_messages(self):
        # Проверка наличия сообщений в контексте
        response = self.client.get(reverse('goods:flower_catalog'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)  # Проверяем, что нет сообщений

    def tearDown(self):
        # Удаляем созданные объекты после тестов
        self.flower1.delete()
        self.flower2.delete()
        self.flower3.delete()
        self.flower4.delete()
        self.flower5.delete()
        self.flower6.delete()
        self.user.delete()