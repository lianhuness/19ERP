# Generated by Django 2.2.4 on 2019-09-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_cofinanceinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cofinanceinfo',
            name='needJiehuiQty',
            field=models.PositiveIntegerField(default=0, verbose_name='TBD Jiehui'),
        ),
    ]