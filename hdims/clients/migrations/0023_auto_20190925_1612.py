# Generated by Django 2.2.4 on 2019-09-25 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0022_clientorder_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientOrderLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('note', models.TextField(blank=True, default='', verbose_name='Note')),
                ('co', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.ClientOrder', verbose_name='Client Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created User')),
            ],
        ),
        migrations.DeleteModel(
            name='CoStatus',
        ),
    ]
