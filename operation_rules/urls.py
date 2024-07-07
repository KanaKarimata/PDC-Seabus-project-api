from django.urls import path
from .views import TimeScheduleCreateView, OperationRuleListView

urlpatterns = [
    path('time-schedule-create/', TimeScheduleCreateView.as_view(), name='time-schedule-create'),
    path('index/', OperationRuleListView.as_view(), name='index'),
]
