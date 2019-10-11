# Generated by Django 2.2.4 on 2019-10-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0024_auto_20191010_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorder',
            name='job_id',
            field=models.CharField(max_length=20, unique=True, verbose_name='Job_ID(Unique)'),
        ),
        migrations.AlterField(
            model_name='clientorder',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('SUBMIT', 'SUBMIT'), ('DELIVER', 'DELIVER'), ('APPROVE', 'APPROVE'), ('COMPLETE', 'COMPLETE'), ('CANCEL', 'CANCEL')], default='DRAFT', max_length=10),
        ),
        migrations.AlterField(
            model_name='cpinfo',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Cost(RMB)'),
        ),
    ]