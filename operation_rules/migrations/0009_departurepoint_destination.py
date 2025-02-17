# Generated by Django 5.0.6 on 2024-07-18 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_rules', '0008_remove_timescheduledetail_operation_status_detail_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeparturePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_point_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=50)),
                ('departure_point', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='operation_rules.departurepoint')),
            ],
        ),
    ]
