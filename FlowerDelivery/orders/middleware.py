from django.http import HttpResponse
from django.utils import timezone

from django.conf import settings

data = settings.COMMON_DICT

class TimeBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем текущее время
        current_time = timezone.localtime(timezone.now()).time()

        # Определяем рабочее время
        start_time = timezone.datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = timezone.datetime.strptime(data['end_time'], '%H:%M').time()
        print(start_time, current_time, end_time)

        # Проверяем доступ к определённым URL
        if request.path in ['/orders/review/', '/orders/form/', '/orders/confirm/']:
            if not (start_time <= current_time <= end_time):
                return HttpResponse(f"Сервис доступен только с {data['start_time']} до {data['end_time']}.")

        response = self.get_response(request)
        return response