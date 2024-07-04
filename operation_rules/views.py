from rest_framework import generics

from .models import TimeSchedule
from .serializers import TimeScheduleSerializer

class TimeScheduleCreateView(generics.CreateAPIView):
  queryset = TimeSchedule.objects.all()
  serializer_class = TimeScheduleSerializer
