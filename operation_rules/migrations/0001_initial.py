# Generated by Django 5.0.6 on 2024-06-30 11:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationRule',
            fields=[
                ('operation_rule_id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_rule_name', models.CharField(max_length=300)),
                ('publish_status_id', models.IntegerField(default=0)),
                ('delete_flg', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OperationStatus',
            fields=[
                ('operation_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('operations_status_type', models.CharField(max_length=100, null=True)),
                ('delete_flg', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OperationStatusDetail',
            fields=[
                ('operation_status_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_status_detail', models.CharField(max_length=100)),
                ('delete_flg', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TimeScheduleDetail',
            fields=[
                ('time_schedule_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('departure_time', models.DateTimeField()),
                ('detail_comment', models.CharField(max_length=40, null=True)),
                ('memo', models.CharField(max_length=500, null=True)),
                ('delete_flg', models.BooleanField(default=False)),
                ('operation_status_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='operation_rules.operationstatusdetail')),
                ('operation_status_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='operation_rules.operationstatus')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSchedule',
            fields=[
                ('time_schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('time_schedule_name', models.CharField(max_length=400)),
                ('publish_start_date', models.DateTimeField(blank=True, null=True)),
                ('publish_end_date', models.DateTimeField(blank=True, null=True)),
                ('delete_flg', models.BooleanField(default=False)),
                ('operation_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation_rules.operationrule')),
                ('update_user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('time_schedule_detail', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='operation_rules.timescheduledetail')),
            ],
        ),
    ]
