# Generated by Django 2.2.4 on 2019-10-17 08:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20191014_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbalance',
            name='balance_date',
            field=models.DateField(default=datetime.date(2019, 10, 17), verbose_name='Balance Date'),
        ),
    ]
