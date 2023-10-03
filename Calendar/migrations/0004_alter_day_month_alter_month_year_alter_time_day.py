# Generated by Django 4.2.4 on 2023-10-03 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0003_alter_day_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='month',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='days', to='Calendar.month'),
        ),
        migrations.AlterField(
            model_name='month',
            name='year',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='months', to='Calendar.year'),
        ),
        migrations.AlterField(
            model_name='time',
            name='day',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='times', to='Calendar.day'),
        ),
    ]
