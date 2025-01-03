from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('use_conditions/', views.conditions, name='use_conditions'),
    path('privacy_policy/', views.privacy, name='privacy_policy'),
]