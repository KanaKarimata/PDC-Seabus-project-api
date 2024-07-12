from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# 運行状況マスタ
class OperationStatus(models.Model):
  operations_status_type = models.CharField(max_length=100, null=True)
  delete_flg = models.BooleanField(default=False)

  def __str__(self):
    return self.operations_status_type

# 運行状況詳細マスタ
class OperationStatusDetail(models.Model):
  operation_status_detail = models.CharField(max_length=100, null=False)
  delete_flg = models.BooleanField(default=False)

  def __str__(self):
    return self.operation_status_detail

# 運行ルールテーブル
class OperationRule(models.Model):
  operation_rule_name = models.CharField(max_length=300, null=False)
  delete_flg = models.BooleanField(default=False)

  def __str__(self):
    return self.operation_rule_name

# 時刻表テーブル
class TimeSchedule(models.Model):
  operation_rule = models.ForeignKey(OperationRule, on_delete=models.CASCADE)
  time_schedule_name = models.CharField(max_length=400, null=False)
  publish_status_id = models.IntegerField(default=0)
  out_of_service_flg = models.BooleanField(default=False)
  publish_start_date = models.DateTimeField(null=True, blank=True)
  publish_end_date = models.DateTimeField(null=True, blank=True)
  update_user = models.ForeignKey(User, models.DO_NOTHING)
  delete_flg = models.BooleanField(default=False)

  def __str__(self):
    return self.time_schedule_name

  def clean(self):
    if self.publish_end_date <= self.publish_start_date:
      return ValidationError(_('公開終了日時は、公開開始日時よりも後の日時を入力してください'))

# スケジュール詳細テーブル
class TimeScheduleDetail(models.Model):
  time_schedule = models.ForeignKey(TimeSchedule, on_delete=models.CASCADE)
  departure_time = models.TimeField(null=True, blank=True)
  operation_status = models.ForeignKey(OperationStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='time_schedule_details')
  operation_status_detail = models.ForeignKey(OperationStatusDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='time_schedule_details')
  detail_comment = models.CharField(max_length=40, null=True, blank=True)
  memo = models.CharField(max_length=500, null=True, blank=True)

# 編集権限テーブル
class EditPermission(models.Model):
  edit_permission_name = models.CharField(max_length=300, unique=True)

  def __str__(self):
    return self.edit_permission_name

# ユーザー権限テーブル
class UserEditPermission(models.Model):
  user = models.ForeignKey(User, models.DO_NOTHING)
  edit_permission = models.ForeignKey(EditPermission, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('user', 'edit_permission')

    def __str__(self):
      return f"{self.user.username} - {self.edit_permission.edit_permission_name}"
