# Generated by Django 4.2.4 on 2023-12-24 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0012_reservations_authority_reservations_success'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservations',
            name='contract',
        ),
    ]