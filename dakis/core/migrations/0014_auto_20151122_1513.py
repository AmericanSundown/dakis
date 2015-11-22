# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151104_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='inner_problem_accuracy',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='inner_problem_division',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='inner_problem_iters',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='lipschitz_estimation',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='neighbours',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='stopping_accuracy',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='stopping_criteria',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='subregion',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='subregion_division',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='subregion_selection',
        ),
    ]
