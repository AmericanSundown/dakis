# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20151218_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='threads',
            field=models.IntegerField(help_text='How many threads are currently running', default=0, null=True, verbose_name='Threads'),
        ),
    ]
