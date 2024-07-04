from rest_framework import serializars
from .models import TimeScheduleDetail, TimeSchedule

class TimeScheduleDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = TimeScheduleDetail
    fields = ['id', 'departure_time', 'operation_status_id', 'operation_status_detail_id', 'detail_comment', 'memo']

class TimeScheduleSerializer(serializers.ModelSerializer):
  time_schedule_detail = TimeScheduleDetailSerializer(read_only = True, many=True)

  class Meta:
    model = TimeSchedule
    fields = ['id', 'operation_rule', 'time_schedule_name', 'publish_status_id', 'out_of_service_flg',  'publish_start_date', 'publish_end_date', 'update_user', 'delete_flg', 'time_schedule_detail']

  def create(self, validated_data):
    time_schedule_detail_data = validated_data.pop('time_schedule_detail')
    time_schedule_instance = TimeSchedule.objects.create(**validated_data)
    for entry in time_schedule_detail_data:
      TimeScheduleDetail.objects.create(time_schedule=time_schedule_instance, **entry)
    return time_schedule_instance