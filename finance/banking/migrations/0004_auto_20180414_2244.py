# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-14 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import finance.banking.models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0003_auto_20180414_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depot',
            name='timespan',
            field=models.ForeignKey(default=finance.banking.models.Timespan.get_default_intelligent_timespan, on_delete=models.SET(finance.banking.models.Timespan.get_default_intelligent_timespan), related_name='depots', to='banking.IntelligentTimespan'),
        ),
    ]
