# Generated by Django 2.2.4 on 2019-10-10 07:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_transfer_abnode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbalance',
            name='balance_date',
            field=models.DateField(default=datetime.date(2019, 10, 10), verbose_name='Balance Date'),
        ),
    ]
