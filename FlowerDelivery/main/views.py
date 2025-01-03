from django.shortcuts import render
from django.conf import settings

data = settings.COMMON_DICT

def index(request):
    return render(request, 'main/index.html', {**data,'active_page': 'index'})

def privacy(request):
    return render(request, 'main/privacy.html', {**data,'active_page': 'privacy'})

def conditions(request):
    return render(request, 'main/conditions.html', {**data,'active_page': 'conditions'})
