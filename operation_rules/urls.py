from django.urls import path
from .views import TimeScheduleCreateView, OperationRuleListView, TimeScheduleListView, TimeScheduleDetailListView, OperationStatusListView, TimeScheduleUpdateView, OperationRuleView

urlpatterns = [
    path('time-schedule-create/', TimeScheduleCreateView.as_view(), name='time-schedule-create'),
    path('index/', OperationRuleListView.as_view(), name='index'),
    path('time-schedule/index/', TimeScheduleListView.as_view(), name='time-schedule-index'),
    path('time-schedule-detail/index/', TimeScheduleDetailListView.as_view(), name="time-schedule-detail-index"),
    path('time-schedule/master/', OperationStatusListView.as_view(), name="time-schedule-master"),
    path('time-schedule-update/<int:pk>/', TimeScheduleUpdateView.as_view(), name="time-schedule-update"),
    path('info/<int:pk>/', OperationRuleView.as_view(), name='info')
]
