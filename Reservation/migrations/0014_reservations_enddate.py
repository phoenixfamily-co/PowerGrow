# Generated by Django 4.2.4 on 2023-12-24 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0013_remove_reservations_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='endDate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
