# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-23 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0006_auto_20180414_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='change',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='banking.Change'),
        ),
    ]
