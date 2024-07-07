from rest_framework import generics

from .models import TimeSchedule, OperationRule
from .serializers import TimeScheduleSerializer, OperationRuleSerializer

class OperationRuleListView(generics.ListAPIView):
  serializer_class = OperationRuleSerializer

  def get_queryset(self):
    return OperationRule.objects.filter(delete_flg=False)

class TimeScheduleCreateView(generics.CreateAPIView):
  queryset = TimeSchedule.objects.all()
  serializer_class = TimeScheduleSerializer

  def create(self, request, *args, **kwargs):
    print("Received data:", request.data)  # デバッグ用
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
