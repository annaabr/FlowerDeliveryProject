from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Импортируем вашу кастомную форму
from .models import Profile
from django.conf import settings

data = settings.COMMON_DICT

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