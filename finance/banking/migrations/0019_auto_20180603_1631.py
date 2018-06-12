# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-03 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0018_auto_20180528_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='banking.Account'),
        ),
    ]