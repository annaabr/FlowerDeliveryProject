from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('review/', views.order_review, name='order_review'),
    path('form/', views.order_form, name='order_form'),
    path('history/', views.order_history, name='order_history'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
]