from django.urls import path
from .views import create_daily_report, view_report, publish_report

urlpatterns = [
    path('create-report/', create_daily_report, name='create_report'),
    path('report/<int:report_id>/', view_report, name='report'),
    path('report/publish/<int:report_id>/', publish_report, name='publish_report'),
]