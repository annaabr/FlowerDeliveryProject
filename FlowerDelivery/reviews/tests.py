from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from goods.models import Flower


class ReviewViewsTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Создаем цветок
        self.flower = Flower.objects.create(name='Test Flower', price=10.00, image='test_image.jpg')
        self.client.login(username='testuser', password='testpass')

    def test_create_review_post_new(self):
        # Проверяем создание нового отзыва
        response = self.client.post(reverse('reviews:create_review', args=[self.flower.id]), {
            'rating': 5,
            'comment': 'Great flower!'
        })
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertEqual(Review.objects.count(), 1)  # Проверяем, что отзыв создан
        review = Review.objects.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great flower!')
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.flower, self.flower)

    def test_create_review_post_edit(self):
        # Создаем отзыв для редактирования
        Review.objects.create(user=self.user, flower=self.flower, rating=3, comment='Average flower.')

        # Проверяем редактирование отзыва
        response = self.client.post(reverse('reviews:create_review', args=[self.flower.id]), {
            'rating': 4,
            'comment': 'Updated review!'
        })
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertEqual(Review.objects.count(), 1)  # Отзыв должен остаться единственным
        review = Review.objects.first()
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Updated review!')

    def test_flower_reviews(self):
        # Создаем отзыв на цветок
        Review.objects.create(user=self.user, flower=self.flower, rating=5, comment='Beautiful flower!')

        # Проверяем отображение отзывов
        response = self.client.get(reverse('reviews:flower_reviews', args=[self.flower.id]))
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ
        self.assertContains(response, 'Beautiful flower!')  # Проверяем, что текст отзыва присутствует в ответе
        self.assertTemplateUsed(response, 'reviews/flower_reviews.html')  # Проверяем, что используется правильный шаблон

    def test_create_review_get(self):
        # Проверка GET запроса на создание отзыва
        response = self.client.get(reverse('reviews:create_review', args=[self.flower.id]))
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ
        self.assertTemplateUsed(response, 'reviews/create_review.html')  # Проверяем, что используется правильный шаблон
        self.assertContains(response, 'Оставить (редактировать) отзыв на Test Flower')  # Проверяем заголовок