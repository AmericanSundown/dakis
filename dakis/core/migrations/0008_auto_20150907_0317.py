# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150907_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='max_duration',
            field=models.FloatField(null=True, verbose_name='Max one execution duration in seconds'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='threads',
            field=models.IntegerField(null=True, verbose_name='Threads', help_text='How many threads are currently running'),
        ),
    ]
