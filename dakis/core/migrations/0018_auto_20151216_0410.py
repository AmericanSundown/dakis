# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_experiment_algorithm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='algorithm_title',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='details',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='executable',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='repository',
        ),
    ]
