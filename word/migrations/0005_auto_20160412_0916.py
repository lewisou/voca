# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0004_auto_20160331_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
