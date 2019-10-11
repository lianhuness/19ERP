# Generated by Django 2.2.4 on 2019-09-18 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('RMB', 'RMB'), ('EUR', 'EUR')], default='RMB', max_length=5, verbose_name='Currency')),
                ('type', models.CharField(choices=[('CORP', 'Corporation'), ('Private', 'Private')], default='CORP', max_length=10, verbose_name='Payee Type')),
                ('note', models.TextField(verbose_name='Note')),
            ],
        ),
    ]