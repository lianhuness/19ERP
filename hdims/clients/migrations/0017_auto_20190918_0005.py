# Generated by Django 2.2.4 on 2019-09-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='note',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Note'),
        ),
    ]