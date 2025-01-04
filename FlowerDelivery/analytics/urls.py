from django.urls import path
from .views import generate_report, report_detail

urlpatterns = [
    path('generate_report/', generate_report, name='generate_report'),
    path('report/<int:report_id>/', report_detail, name='report_detail'),
]