from rest_framework import generics

from .models import TimeSchedule
from .serializers import TimeScheduleSerializer

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
