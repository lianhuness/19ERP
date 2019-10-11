# Generated by Django 2.2.4 on 2019-09-24 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_clientcontactor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorder',
            name='contactor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.ClientContactor', verbose_name='Client Contactor'),
        ),
    ]
