# Generated by Django 5.0.6 on 2024-07-04 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_rules', '0003_rename_operation_rule_timeschedule_operation_rule_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeschedule',
            old_name='operation_rule_id',
            new_name='operation_rule',
        ),
        migrations.RenameField(
            model_name='timeschedule',
            old_name='update_user_id',
            new_name='update_user',
        ),
        migrations.RemoveField(
            model_name='operationrule',
            name='operation_rule_id',
        ),
        migrations.RemoveField(
            model_name='operationstatus',
            name='operation_status_id',
        ),
        migrations.RemoveField(
            model_name='operationstatusdetail',
            name='operation_status_detail_id',
        ),
        migrations.RemoveField(
            model_name='timeschedule',
            name='time_schedule_detail_id',
        ),
        migrations.RemoveField(
            model_name='timeschedule',
            name='time_schedule_id',
        ),
        migrations.RemoveField(
            model_name='timescheduledetail',
            name='time_schedule_detail_id',
        ),
        migrations.AddField(
            model_name='operationrule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operationstatus',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operationstatusdetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeschedule',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timescheduledetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timescheduledetail',
            name='time_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation_rules.timeschedule'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timescheduledetail',
            name='operation_status_detail_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='timescheduledetail',
            name='operation_status_id',
            field=models.IntegerField(null=True),
        ),
    ]
