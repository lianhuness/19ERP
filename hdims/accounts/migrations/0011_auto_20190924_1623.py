# Generated by Django 2.2.4 on 2019-09-24 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190924_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['payment_date', 'updated_time']},
        ),
    ]