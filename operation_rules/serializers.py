from rest_framework import serializars
from .models import OperationRule, TimeScheduleDetail, TimeSchedule

class OperationRuleSerializer(serializers.ModelSerializer):
  class Meta:
    model = OperationRule
    fields = ['operation_rule_id', 'operation_rule_name', 'delete_flg']

class TimeScheduleDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = TimeScheduleDetail
    fields = ['time_schedule_detail_id', 'departure_time', 'operation_status_id', 'operation_status_detail_id', 'detail_comment', 'memo', 'delete_flg']

class TimeScheduleSerializer(serializers.ModelSerializer):
  time_schedule_detail_set = TimeScheduleDetailSerializer(read_only = True, many=True)

  class Meta:
    model = TimeSchedule
    fields = ['time_schedule_id', 'operation_rule', 'time_schedule_name', 'publish_status_id', 'time_schedule_detail', 'publish_start_date', 'publish_end_date', 'update_user_id', 'delete_flg']