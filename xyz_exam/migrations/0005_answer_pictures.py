# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-09-01 23:06
from __future__ import unicode_literals

from django.db import migrations
import xyz_util.modelutils


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20200802_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='pictures',
            field=xyz_util.modelutils.JSONField(blank=True, default={}, verbose_name='\u56fe\u7247'),
        ),
    ]
