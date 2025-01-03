from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from goods.models import Flower
from django.contrib import messages
from django.conf import settings

data = settings.COMMON_DICT


def create_review(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flower = flower
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('goods:flower_catalog')  # Перенаправление на страницу каталога
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html',
                  {**data, 'flower': flower, 'form': form, 'active_page': 'create_review'})

def flower_reviews(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    reviews = Review.objects.filter(flower=flower).order_by('-created_at')  # Сортируем по убыванию даты создания

    return render(request, 'reviews/flower_reviews.html', {**data, 'flower': flower, 'reviews': reviews, 'active_page': 'flower_reviews'})

# def flower_reviews(request, flower_id):
    #     flower = get_object_or_404(Flower, id=flower_id)
    # reviews = Review.objects.filter(flower=flower)

    # return render(request, 'reviews/flower_reviews.html', {**data, 'flower': flower, 'reviews': reviews, 'active_page': 'flower_reviews'})

