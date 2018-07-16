# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-17 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0019_auto_20180603_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='banking.Account'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='banking.Category'),
        ),
    ]