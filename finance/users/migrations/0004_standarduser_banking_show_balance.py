# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-23 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_standarduser_rounded_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarduser',
            name='banking_show_balance',
            field=models.BooleanField(default=False),
        ),
    ]
