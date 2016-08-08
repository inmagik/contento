# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 22:11
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contento', '0003_page_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='content',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='page',
            name='data',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]