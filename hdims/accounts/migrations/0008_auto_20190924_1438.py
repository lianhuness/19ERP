# Generated by Django 2.2.4 on 2019-09-24 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190920_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-payment_date', '-updated_time']},
        ),
    ]