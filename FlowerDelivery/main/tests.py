from django.test import TestCase
from django.urls import reverse
from django.conf import settings

class ViewsTestCase(TestCase):
    def setUp(self):
        # Установим переменные для использования в тестах
        self.data = settings.COMMON_DICT
        self.data['caption'] = 'Тестовый магазин'
        self.data['start_time'] = '9:00'
        self.data['end_time'] = '21:00'

    def test_index_view(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertIn('active_page', response.context)
        self.assertEqual(response.context['active_page'], 'index')
        self.assertEqual(response.context['caption'], self.data['caption'])

    def test_privacy_view(self):
        response = self.client.get(reverse('main:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/privacy.html')
        self.assertIn('active_page', response.context)
        self.assertEqual(response.context['active_page'], 'privacy')
        self.assertEqual(response.context['caption'], self.data['caption'])

    def test_conditions_view(self):
        response = self.client.get(reverse('main:use_conditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/conditions.html')
        self.assertIn('active_page', response.context)
        self.assertEqual(response.context['active_page'], 'conditions')
        self.assertEqual(response.context['caption'], self.data['caption'])