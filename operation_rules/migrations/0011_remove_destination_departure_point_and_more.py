# Generated by Django 5.0.6 on 2024-07-18 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation_rules', '0010_timeschedule_destination_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='departure_point',
        ),
        migrations.RenameField(
            model_name='destination',
            old_name='destination',
            new_name='destination_name',
        ),
        migrations.AlterField(
            model_name='timeschedule',
            name='destination',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.DO_NOTHING, to='operation_rules.destination'),
        ),
        migrations.DeleteModel(
            name='DeparturePoint',
        ),
    ]
