# Generated by Django 2.2.4 on 2019-09-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_auto_20190924_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientorder',
            name='job_id',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='Job_ID'),
            preserve_default=False,
        ),
    ]
