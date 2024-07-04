from django.urls import path
from .view import TimeScheduleCreateView

urlpatterns = [
    path('time-schedule-create/', TimeScheduleCreateView.as_View(), name='time-schedule-create')
]
