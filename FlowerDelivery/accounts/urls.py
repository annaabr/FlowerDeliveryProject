from django.urls import path
from .views import CustomLoginView  # Импортируем ваш кастомный класс
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Используем кастомный класс
    path('logout/', LogoutView.as_view(next_page='main:index'), name='logout'),
    path('profile/', views.profile, name='profile')
]