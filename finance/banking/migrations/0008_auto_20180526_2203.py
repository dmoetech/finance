# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-26 20:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0007_auto_20180523_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timespan',
            name='timespan',
        ),
        migrations.DeleteModel(
            name='Timespan',
        ),
    ]
