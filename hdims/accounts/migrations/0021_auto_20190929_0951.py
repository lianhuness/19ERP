# Generated by Django 2.2.4 on 2019-09-29 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_cosummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosummary',
            name='rmbProfitRatio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='利润率'),
        ),
        migrations.DeleteModel(
            name='CoFinanceInfo',
        ),
    ]
