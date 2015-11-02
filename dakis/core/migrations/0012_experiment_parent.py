# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151102_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, to='core.Experiment', related_name='children'),
        ),
    ]
