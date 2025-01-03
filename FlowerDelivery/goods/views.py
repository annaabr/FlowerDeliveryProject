from django.shortcuts import render
from .models import Flower
from django.conf import settings
from django.contrib.messages import get_messages
from django.db.models import Avg

#from reviews.models import Review

data = settings.COMMON_DICT

def catalog(request):
    flowers = Flower.objects.all().annotate(average_rating=Avg('review__rating'))  # Получаем все товары из базы данных
    messages = get_messages(request)  # Получаем сообщения из запроса
    return render(request, 'main/catalog.html',
                  {**data,'messages': messages,'flowers': flowers, 'active_page': 'catalog'})