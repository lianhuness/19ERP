# Generated by Django 2.2.4 on 2019-09-09 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Product Name')),
                ('priceUSD', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price(USD)')),
                ('priceTerm', models.CharField(choices=[('FOB', 'FOB'), ('EXW', 'EXW'), ('ST', 'Tax + Shipping'), ('S', 'Shipping Only(No Tax)'), ('T', 'Tax(No Shipping')], default='FOB', max_length=5, verbose_name='Price Term')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
            ],
        ),
    ]
