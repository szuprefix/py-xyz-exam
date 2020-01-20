#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:denishuang

from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'xyz_exam'
    label = 'exam'
    verbose_name = '测验'

    def ready(self):
        super(Config, self).ready()
        from . import receivers