# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-08 10:57
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20170307_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='\u8be6\u7ec6\u63cf\u8ff0'),
        ),
    ]
