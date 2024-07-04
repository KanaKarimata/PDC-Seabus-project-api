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
  departure_time = models.DateTimeField(null=False)
  operation_status_id = models.IntegerField(null=True)
  operation_status_detail_id = models.IntegerField(null=True)
  detail_comment = models.CharField(max_length=40, null=True)
  memo = models.CharField(max_length=500, null=True)

