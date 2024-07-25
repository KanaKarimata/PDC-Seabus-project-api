from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime, date, timezone
import pytz
from django.utils.timezone import localtime

from .models import TimeSchedule, OperationRule, UserEditPermission, TimeScheduleDetail, OperationStatus, OperationStatusDetail, Destination
from .serializers import TimeScheduleSerializer, OperationRuleSerializer, UserEditPermissionSerializer, TimeScheduleDetailSerializer, OperationStatusMasterSerializer, OperationStatusDetailMasterSerializer, DestinationMasterSerializer
from .enums import DeparturePointEnum

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
      return TimeSchedule.objects.filter(operation_rule_id=operation_rule_id, delete_flg=False).order_by('-publish_status_id')
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

    if time_schedule_id is None:
      raise ValueError("idパラメータが不正です")

    try:
      return TimeScheduleDetail.objects.filter(time_schedule_id=time_schedule_id).order_by('departure_time')
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

    destination_queryset = Destination.objects.all()
    destination_serializer = DestinationMasterSerializer(destination_queryset, many=True)
    destination_data = destination_serializer.data

    print("Throwing data:", serializer.data)

    return Response({
      'time_schedule': time_schedule_serializer.data if time_schedule else None,
      'scheduleDetails': serializer.data,
      'operation_status': operation_status_data,
      'operation_status_detail': operation_status_detail_data,
      'destination': destination_data
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
    # 日本標準時（JST）のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')

    publish_start_date = serializer.validated_data['publish_start_date'].astimezone(jst)
    publish_end_date = serializer.validated_data['publish_end_date'].astimezone(jst)

    # タイムゾーンをJSTに変更して保存
    return serializer.save(
        publish_start_date=publish_start_date,
        publish_end_date=publish_end_date,
        update_user=self.request.user
    )

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
     # 日本標準時（JST）のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')

    publish_start_date = serializer.validated_data['publish_start_date'].astimezone(jst)
    publish_end_date = serializer.validated_data['publish_end_date'].astimezone(jst)
    # タイムゾーンをJSTに変更して保存
    serializer.save(
        publish_start_date=publish_start_date,
        publish_end_date=publish_end_date,
        update_user=self.request.user
    )

  def update(self, request, *arg, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)

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

    destination_queryset = Destination.objects.all()
    destination_serializer = DestinationMasterSerializer(destination_queryset, many=True)
    destination_data = destination_serializer.data

    print('destination_data', destination_data)

    return Response({
      'operation_status': operation_status_data,
      'operation_status_detail': operation_status_detail_data,
      'destination' : destination_data
    }, status=status.HTTP_200_OK)

# 時刻表削除処理
class TimeScheduleDestroyView(generics.DestroyAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = TimeScheduleSerializer

  def get_queryset(self):
    id = self.kwargs['pk']
    return TimeSchedule.objects.filter(id=id)

# デジタルサイネージ用時刻表データ取得
class SignageTimeScheduleListView(generics.ListAPIView):
  serializer_class = TimeScheduleDetailSerializer

  def get_queryset(self):
    time_schedule_id = self.request.query_params.get('time_schedule_id')

    if time_schedule_id is None:
        return TimeScheduleDetail.objects.none()

    try:
      return TimeScheduleDetail.objects.filter(
          time_schedule_id=time_schedule_id,
        ).order_by('departure_time')
    except ValueError as e:
      return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)

    time_schedule_id = request.query_params.get('time_schedule_id')
    operation_rule_id = request.query_params.get('operation_rule_id')
    time_schedule = None
    time_schedule_serializer = None

    if time_schedule_id and operation_rule_id:
      jst = pytz.timezone('Asia/Tokyo')
      today = datetime.now(tz=jst)
      weekday = today.weekday()
      today_date = today
      # 土日の場合
      if (weekday == 5) or (weekday == 6):
        time_schedule = TimeSchedule.objects.filter(
                  id=time_schedule_id,
                  operation_rule_id=operation_rule_id,
                  publish_holiday_flg=True,
                  publish_status_id=1).first()
        if time_schedule:
          publish_start_date_jst = localtime(time_schedule.publish_start_date, jst)
          publish_end_date_jst = localtime(time_schedule.publish_end_date, jst)
          if publish_start_date_jst <= today_date <= publish_end_date_jst:
            time_schedule_serializer = TimeScheduleSerializer(time_schedule)
      # 平日の場合
      else:
        time_schedule = TimeSchedule.objects.filter(
                  id=time_schedule_id,
                  operation_rule_id=operation_rule_id,
                  publish_holiday_flg=False,
                  publish_status_id=1).first()
        if time_schedule:
          publish_start_date_jst = localtime(time_schedule.publish_start_date, jst)
          publish_end_date_jst = localtime(time_schedule.publish_end_date, jst)
          if publish_start_date_jst <= today_date <= publish_end_date_jst:
            time_schedule_serializer = TimeScheduleSerializer(time_schedule)

    print("Throwing data:", serializer.data)
    print("Throwing data:", time_schedule_serializer.data if time_schedule_serializer else None)
    time_schedule_serializer_data = None
    time_schedule_detail_data = []
    if time_schedule_serializer:
      time_schedule_serializer_data = time_schedule_serializer.data
      time_schedule_detail_data = serializer.data

    return Response({
      'time_schedule': time_schedule_serializer_data if time_schedule else None,
      'scheduleDetails': time_schedule_detail_data
    }, status=status.HTTP_200_OK)

# デジタルサイネージ用次の出発時刻データ取得
class SignageNextDepartureListView(generics.ListAPIView):
  serializer_class = TimeScheduleDetailSerializer

  def get_queryset(self):
    operation_rule_id = self.kwargs['operation_rule_id']
    destination = self.kwargs['destination']

    operation_rule = get_object_or_404(OperationRule, id=operation_rule_id)

    jst = pytz.timezone('Asia/Tokyo')
    today = datetime.now(tz=jst)
    weekday = today.weekday()
    now = datetime.now(jst)
    current_time = now.time()
    time_schedules = None

    publish_holiday_flg = weekday == 5 or weekday == 6

    time_schedules_sub = TimeSchedule.objects.filter(
            operation_rule=operation_rule,
            destination=destination,
            publish_holiday_flg=publish_holiday_flg,
            publish_status_id=1)
    print('Got time_schedule', time_schedules_sub)

    for t in time_schedules_sub:
      publish_start_date = t.publish_start_date.astimezone(jst)
      publish_end_date = t.publish_end_date.astimezone(jst)

      if publish_start_date <= now <= publish_end_date:
        time_schedules = TimeSchedule.objects.filter(
              operation_rule=operation_rule,
              destination=destination,
              publish_holiday_flg=publish_holiday_flg,
              publish_status_id=1)

    time_schedule_details = None
    if time_schedules:
      time_schedule_details = TimeScheduleDetail.objects.filter(
          time_schedule__in=time_schedules,
          operation_status=1,
          departure_time__gt=current_time
      ).order_by('departure_time')

    # 現在の時刻よりも直後の時刻を取得
    if time_schedule_details:
        # 最初のレコードを取得
        first_departure = time_schedule_details.first()
        return TimeScheduleDetail.objects.filter(
            id=first_departure.id
        )
    return TimeScheduleDetail.objects.none()

  def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'next_departure_time': None}, status=status.HTTP_200_OK)
