from django.urls import path
from .views import TimeScheduleCreateView, OperationRuleListView, TimeScheduleListView, TimeScheduleDetailListView

urlpatterns = [
    path('time-schedule-create/', TimeScheduleCreateView.as_view(), name='time-schedule-create'),
    path('index/', OperationRuleListView.as_view(), name='index'),
    path('time-schedule/index/', TimeScheduleListView.as_view(), name='time-schedule-index'),
    path('time-schedule-detail/index/', TimeScheduleDetailListView.as_view(), name="time-schedule-detail-index")
]
