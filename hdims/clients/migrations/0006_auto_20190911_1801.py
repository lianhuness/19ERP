# Generated by Django 2.2.4 on 2019-09-11 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0005_auto_20190911_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientproduct',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='price',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='priceRMB',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='priceTerm',
        ),
        migrations.AddField(
            model_name='clientproduct',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientproduct',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='productprice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('RMB', 'RMB'), ('EUR', 'EUR')], default='USD', max_length=5)),
                ('priceTerm', models.CharField(choices=[('FOB', 'FOB'), ('EXW', 'EXW'), ('ST', 'Tax + Shipping'), ('S', 'Shipping Only(No Tax)'), ('T', 'Tax(No Shipping')], default='FOB', max_length=5, verbose_name='Price Term')),
                ('priceRMB', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price(RMB)')),
                ('cp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.ClientProduct', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
