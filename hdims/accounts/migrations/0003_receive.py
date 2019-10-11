# Generated by Django 2.2.4 on 2019-09-18 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_auto_20190918_0005'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_payee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('RMB', 'RMB'), ('EUR', 'EUR')], default='USD', max_length=5, verbose_name='Currency')),
                ('payer', models.CharField(max_length=100, verbose_name='Payer Name')),
                ('note', models.TextField(verbose_name='Note')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account', verbose_name='Account')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client', verbose_name='Client')),
                ('clientorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.ClientOrder', verbose_name='Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]