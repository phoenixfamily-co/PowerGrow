# Generated by Django 4.2.4 on 2023-10-04 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0005_alter_day_month_alter_month_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='month',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='times', to='Calendar.day'),
        ),
        migrations.AlterField(
            model_name='year',
            name='name',
            field=models.CharField(blank=True, choices=[('جلالی', 'Jalali'), ('میلادی', 'Gregorian'), ('قمری', 'Lunar')], max_length=20, null=True),
        ),
    ]
