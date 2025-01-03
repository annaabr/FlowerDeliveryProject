from django.urls import path
from .views import create_review, flower_reviews

app_name = 'reviews'

urlpatterns = [
    path('create/<int:flower_id>/', create_review, name='create_review'),
    path('flower/<int:flower_id>/reviews/', flower_reviews, name='flower_reviews'),
]