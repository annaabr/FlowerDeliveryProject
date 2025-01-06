from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class AccountsViewsTests(TestCase):

    def setUp(self):
        self.register_url = reverse('accounts:register')
        self.profile_url = reverse('accounts:profile')
        self.cart_view_url = reverse('cart:cart_view')  # Добавляем URL для cart_view

    def test_register_user_invalid(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',  # Несоответствие паролей
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 200)  # Должен вернуть на страницу регистрации
        form = response.context['form']  # Получаем форму из контекста ответа
        self.assertTrue(form.errors)  # Проверяем наличие ошибок в форме
        self.assertEqual(form.errors['password2'], ['Введенные пароли не совпадают.'])  # Проверяем сообщение об ошибке

    def test_profile_view_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.client.login(username='testuser', password='testpassword123')  # Логин пользователя
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница профиля загружается корректно
        self.assertTemplateUsed(response, 'accounts/profile.html')  # Убедимся в использовании правильного шаблона

    def test_update_profile(self):
        user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.client.login(username='testuser', password='testpassword123')
        profile = Profile.objects.create(user=user, phone='', address='')

        response = self.client.post(self.profile_url, {
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, 302)  # Должен перенаправить после сохранения
        user.refresh_from_db()  # Обновляем экземпляр пользователя
        profile.refresh_from_db()  # Обновляем экземпляр профиля
        self.assertEqual(user.email, 'newemail@example.com')  # Проверяем обновление email
        self.assertEqual(profile.phone, '1234567890')  # Проверяем обновление телефона
        self.assertEqual(profile.address, 'New Address')  # Проверяем обновление адреса