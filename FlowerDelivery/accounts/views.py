from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Импортируем вашу кастомную форму
from .models import Profile
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

data = settings.COMMON_DICT

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('cart:cart_view')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Сохраняем сессию пользователя
            return redirect('main:index')  # Переход на страницу после успешной смены пароля
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {**data, 'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(settings.COMMON_DICT)
        return context

    def get_success_url(self):
        return reverse_lazy('goods:flower_catalog')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Используем CustomUserCreationForm
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя через кастомную форму
            login(request, user)  # Логиним пользователя
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()  # Создаем пустую форму при GET-запросе
    return render(request, 'accounts/register.html', {**data, 'form': form, 'acitve_page': 'register'})

def profile(request):
    # Проверка, аутентифицирован ли пользователь
    if not request.user.is_authenticated:
        return redirect('cart:cart_view')  # Перенаправление незалогиненного пользователя на страницу cart:cart_view

    profile, created = Profile.objects.get_or_create(user=request.user)  # Получаем или создаем профиль пользователя
    if request.method == 'POST':
        # Обработка формы редактирования профиля
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        request.user.email = request.POST.get('email')
        request.user.save()
        profile.save()
        return redirect('main:index')  # Перенаправление на главную страницу после сохранения изменений

    return render(request, 'accounts/profile.html', {**data, 'profile': profile, 'acitve_page': 'register'})

