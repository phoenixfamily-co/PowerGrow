# Generated by Django 4.2.4 on 2023-10-16 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_user_accountid_user_accountnumber_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='accountId',
            field=models.TextField(blank=True, default='شماره شبا', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='accountNumber',
            field=models.TextField(blank=True, default='شماره حساب', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, default='آدرس', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default='ایمیل', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.IntegerField(blank=True, default='تلفن ثابت', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='zipCode',
            field=models.IntegerField(blank=True, default='کدپستی', null=True),
        ),
    ]
