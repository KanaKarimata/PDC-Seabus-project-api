from rest_framework import serializers
from .models import TimeScheduleDetail, TimeSchedule, OperationRule, UserEditPermission, EditPermission
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class EditPermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = EditPermission
    fields = ['id', 'edit_permission_name']

class UserEditPermissionSerializer(serializers.ModelSerializer):
  edit_permission = EditPermissionSerializer()

  class Meta:
    model = UserEditPermission
    fields = ['edit_permission']

class OperationRuleSerializer(serializers.ModelSerializer):
  class Meta:
    model = OperationRule
    fields = ['id', 'operation_rule_name']

  def get_user_edit_permissions(self, obj):
    user = self.context(['request']).user
    user_edit_permissions = UserEditPermission.objects.filter(user=user)
    return UserEditPermissionSerializer(user_edit_permissions, many=True).data

class TimeScheduleSerializer(serializers.ModelSerializer):
  update_user = UserSerializer(read_only=True)

  class Meta:
    model = TimeSchedule
    fields = ['id', 'operation_rule', 'time_schedule_name', 'publish_status_id', 'out_of_service_flg',  'publish_start_date', 'publish_end_date', 'update_user', 'delete_flg']

class TimeScheduleDetailSerializer(serializers.ModelSerializer):
  departure_time = serializers.DateTimeField(allow_null=True, required=False)
  detail_comment = serializers.CharField(allow_null=True, required=False)
  memo = serializers.CharField(allow_null=True, required=False)
  time_schedule = TimeScheduleSerializer(required=True)

  class Meta:
    model = TimeScheduleDetail
    fields = ['id', 'time_schedule', 'departure_time', 'operation_status_id', 'operation_status_detail_id', 'detail_comment', 'memo']
