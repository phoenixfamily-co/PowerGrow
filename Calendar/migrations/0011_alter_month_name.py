# Generated by Django 4.2.4 on 2024-04-12 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calendar', '0010_time_res_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
