# Generated by Django 2.2.4 on 2019-08-20 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gameSite', '0018_delete_stand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standID', models.CharField(max_length=20, verbose_name='機台代碼')),
                ('standDesc', models.CharField(max_length=120, verbose_name='機台說明')),
                ('standPrice', models.FloatField(default=0, verbose_name='機台價格')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='負責人')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gameSite.Location', verbose_name='安裝地點')),
            ],
            options={
                'verbose_name': '機台',
                'verbose_name_plural': '機台',
            },
        ),
    ]
