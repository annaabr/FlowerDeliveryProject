from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('review/', views.order_review, name='order_review'),
    path('form/', views.order_form, name='order_form'),
    path('confirm/', views.confirm_order, name='confirm_order'),
]