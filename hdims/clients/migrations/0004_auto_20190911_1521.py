# Generated by Django 2.2.4 on 2019-09-11 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20190911_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
    ]
