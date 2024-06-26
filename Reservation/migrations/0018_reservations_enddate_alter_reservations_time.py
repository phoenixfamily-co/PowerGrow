# Generated by Django 4.2.4 on 2024-05-31 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0011_alter_month_name'),
        ('Reservation', '0017_remove_reservations_enddate_alter_reservations_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='endDate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations_End', to='Calendar.time'),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations_Start', to='Calendar.time'),
        ),
    ]
