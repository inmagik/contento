# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-20 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contento', '0007_auto_20161020_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='fullpath',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
