from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart-view/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
 ]