# Generated by Django 4.2.4 on 2024-01-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0009_time_off_time_price'),
        ('Product', '0017_participants_startday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participants',
            name='startDay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='Calendar.day'),
        ),
    ]