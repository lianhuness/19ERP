# Generated by Django 2.2.4 on 2019-09-12 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20190912_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpprice',
            name='cp',
        ),
        migrations.RemoveField(
            model_name='cpprice',
            name='user',
        ),
        migrations.DeleteModel(
            name='CPCost',
        ),
        migrations.DeleteModel(
            name='CPPrice',
        ),
    ]
