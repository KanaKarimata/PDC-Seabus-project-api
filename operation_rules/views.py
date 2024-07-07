from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TimeSchedule, OperationRule, UserEditPermission
from .serializers import TimeScheduleSerializer, OperationRuleSerializer, UserEditPermissionSerializer

class OperationRuleListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = OperationRuleSerializer

  def get_queryset(self):
    return OperationRule.objects.filter(delete_flg=False)
  
  def get(self, request, *args, **kwargs):
    try:
      response = super().get(request, *args, **kwargs)
      user_edit_permissions = UserEditPermission.objects.filter(user=request.user)
      user_edit_permissions_data = UserEditPermissionSerializer(user_edit_permissions, many=True).data
      response.data = {
        'operation_rules': response.data,
        'user_permissions': user_edit_permissions_data
      }
      return response
    except Exception as e:
      return Response({'error': str(e)}, status=500)

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
