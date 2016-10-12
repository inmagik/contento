# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-12 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contento', '0005_auto_20160920_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='page',
            name='data',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='page',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]