# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150822_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(verbose_name='Status', default='C', choices=[('C', 'Created'), ('R', 'Running'), ('S', 'Suspended'), ('D', 'Done')], max_length=2),
        ),
    ]
