# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-11 11:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import finance.crypto.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crypto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='intelligenttimespan',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='crypto_intelligent_timespans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='depot',
            name='timespan',
            field=models.ForeignKey(on_delete=models.SET(finance.crypto.models.Timespan.get_default_intelligent_timespan), related_name='depots', to='crypto.IntelligentTimespan'),
        ),
        migrations.AddField(
            model_name='depot',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='crypto_depots', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='depot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to='crypto.Depot'),
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together=set([('asset', 'date', 'currency')]),
        ),
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together=set([('depot', 'account', 'asset')]),
        ),
    ]
