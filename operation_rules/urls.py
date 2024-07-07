from django.urls import path
from .views import TimeScheduleCreateView

urlpatterns = [
    path('time-schedule-create/', TimeScheduleCreateView.as_view(), name='time-schedule-create')
]
