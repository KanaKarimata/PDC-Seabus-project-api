from rest_framework import viewsets

from .models import OperationRule, TimeSchedule
from .serializers import OperationRuleSerializer, TimeScheduleSerializer

class OperationRuleSet(viewsets.ModelViewSet):
  queryset = OperationRule.objects.all()
  serializer_class = OperationRuleSerializer

class TimeScheduleSet(viewsets.ModelViewSet):
  queryset = TimeSchedule.objects.prefetch_related('time_schedule_detail_set').all()
  serializer_class = TimeScheduleSerializer
