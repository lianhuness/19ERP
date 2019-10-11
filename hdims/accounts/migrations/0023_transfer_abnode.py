# Generated by Django 2.2.4 on 2019-09-29 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_accountbalance'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='abnode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountBalance', verbose_name='Account Balance Node'),
        ),
    ]
