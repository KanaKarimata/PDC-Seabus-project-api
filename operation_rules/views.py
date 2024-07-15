from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.db import transaction

from .models import TimeSchedule, OperationRule, UserEditPermission, TimeScheduleDetail, OperationStatus, OperationStatusDetail
from .serializers import TimeScheduleSerializer, OperationRuleSerializer, UserEditPermissionSerializer, TimeScheduleDetailSerializer, OperationStatusMasterSerializer, OperationStatusDetailMasterSerializer

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

# 運航ルール名表示
class OperationRuleView(generics.RetrieveAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = OperationRuleSerializer
  lookup_field = 'pk'

  def get_queryset(self):
    operation_rule_id = self.kwargs.get('pk')

    if operation_rule_id is None:
      raise ValueError("idパラメータが不正です")

    try:
      return OperationRule.objects.filter(id=operation_rule_id, delete_flg=False)
    except ValueError as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

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

# 時刻表詳細一覧表示
class TimeScheduleDetailListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleDetailSerializer

  def get_queryset(self):
    time_schedule_id = self.request.query_params.get('time_schedule_id')
    print(time_schedule_id)

    if time_schedule_id is None:
      raise ValueError("idパラメータが不正です")

    try:
      return TimeScheduleDetail.objects.filter(time_schedule_id=time_schedule_id)
    except ValueError as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)

    time_schedule_id = request.query_params.get('time_schedule_id')
    time_schedule = None
    if time_schedule_id:
        time_schedule = TimeSchedule.objects.filter(id=time_schedule_id).first()
        if time_schedule:
            time_schedule_serializer = TimeScheduleSerializer(time_schedule)

    operation_status_queryset = OperationStatus.objects.filter(delete_flg=False)
    operation_status_serializer = OperationStatusMasterSerializer(operation_status_queryset, many=True)
    operation_status_data = operation_status_serializer.data

    operation_status_detail_queryset = OperationStatusDetail.objects.filter(delete_flg=False)
    operation_status_detail_serializer = OperationStatusDetailMasterSerializer(operation_status_detail_queryset, many=True)
    operation_status_detail_data = operation_status_detail_serializer.data

    print("Throwing data:", serializer.data)

    return Response({
      'time_schedule': time_schedule_serializer.data if time_schedule else None,
      'scheduleDetails': serializer.data,
      'operation_status': operation_status_data,
      'operation_status_detail': operation_status_detail_data
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

# 時刻表更新処理
class TimeScheduleUpdateView(generics.UpdateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleSerializer

  def get_queryset(self):
     return TimeSchedule.objects.all()
  
  def perform_update(self, serializer):
     serializer.save(update_user=self.request.user)
  
  def update(self, request, *arg, **kwargs):
    print("update:", request.data)  # デバッグ用
    instance = self.get_object()
    print("instance:", request.data)  # デバッグ用
    serializer = self.get_serializer(instance, data=request.data)
    print("serializer:", request.data)  # デバッグ用
    serializer.is_valid(raise_exception=True)
    print("error:", serializer.errors)
    print("is_valid:", request.data)  # デバッグ用
    self.perform_update(serializer)
    print("perform_update:", request.data)  # デバッグ用

    with transaction.atomic():
      self.perform_update(serializer)

      time_schedule_details = request.data.get('time_schedule_detail', [])
      print("get:", request.data)  # デバッグ用

      for detail_data in time_schedule_details:
        if detail_data['id'] is not None:
          TimeScheduleDetail.objects.filter(id=detail_data['id']).update(
            departure_time=detail_data.get('departure_time'),
            operation_status_id=detail_data.get('operation_status_id'),
            operation_status_detail_id=detail_data.get('operation_status_detail_id'),
            detail_comment=detail_data.get('detail_comment'),
            memo=detail_data.get('memo')
          )
        else:
          TimeScheduleDetail.objects.create(
              time_schedule=instance,
              departure_time=detail_data.get('departure_time'),
              operation_status_id=detail_data.get('operation_status_id'),
              operation_status_detail_id=detail_data.get('operation_status_detail_id'),
              detail_comment=detail_data.get('detail_comment'),
              memo=detail_data.get('memo')
          )
    return Response(serializer.data, status=status.HTTP_200_OK)


# マスタデータ取得
class OperationStatusListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request, *args, **kwargs):
    operation_status_queryset = OperationStatus.objects.filter(delete_flg=False)
    operation_status_serializer = OperationStatusMasterSerializer(operation_status_queryset, many=True)
    operation_status_data = operation_status_serializer.data

    operation_status_detail_queryset = OperationStatusDetail.objects.filter(delete_flg=False)
    operation_status_detail_serializer = OperationStatusDetailMasterSerializer(operation_status_detail_queryset, many=True)
    operation_status_detail_data = operation_status_detail_serializer.data

    return Response({
      'operation_status': operation_status_data,
      'operation_status_detail': operation_status_detail_data
    }, status=status.HTTP_200_OK)

# 時刻表削除処理
class TimeScheduleDestroyView(generics.DestroyAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleSerializer

  def get_queryset(self):
    id = self.kwargs['pk']
    return TimeSchedule.objects.filter(id=id)

