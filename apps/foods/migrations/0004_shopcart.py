# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 08:51
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foods', '0003_auto_20170308_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.Food', verbose_name='\u83dc\u5355')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u8d2d\u7269\u8f66',
                'verbose_name_plural': '\u8d2d\u7269\u8f66',
            },
        ),
    ]
