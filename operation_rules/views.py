from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import TimeSchedule, OperationRule, UserEditPermission, TimeScheduleDetail
from .serializers import TimeScheduleSerializer, OperationRuleSerializer, UserEditPermissionSerializer

# 運航ルール一覧表示
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

# 時刻表一覧表示
class TimeScheduleListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleSerializer

  def get_queryset(self):
    operation_rule_id = self.request.query_params.get('operation_rule_id')

    if operation_rule_id is None:
      raise ValueError("idパラメータが不正です")

    try:
      return TimeSchedule.objects.filter(operation_rule_id=operation_rule_id, delete_flg=False)
    except ValueError as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        operation_rule_id = request.query_params.get('operation_rule_id')
        operation_rule_name = None
        if operation_rule_id:
            operation_rule = OperationRule.objects.filter(id=operation_rule_id).first()
            if operation_rule:
                operation_rule_name = operation_rule.operation_rule_name

        return Response({
            'operation_rule_name': operation_rule_name,
            'schedules': serializer.data
        }, status=status.HTTP_200_OK)

# 時刻表作成
class TimeScheduleCreateView(generics.CreateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    print("Received data:", request.data)  # デバッグ用
    serializer.is_valid(raise_exception=True)
    time_schedule_instance = self.perform_create(serializer)
    
    # Create TimeScheduleDetail instances
    time_schedule_details = request.data.get('time_schedule_detail', [])
    for detail_data in time_schedule_details:
      TimeScheduleDetail.objects.create(time_schedule=time_schedule_instance, **detail_data)

    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  def perform_create(self, serializer):
    return serializer.save(update_user=self.request.user)

  def get_success_headers(self, data):
    try:
        return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    except (TypeError, KeyError):
        return {}