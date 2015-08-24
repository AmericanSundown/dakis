# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_experiment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='simplex_division',
        ),
        migrations.AddField(
            model_name='experiment',
            name='subregion_division',
            field=models.CharField(max_length=255, help_text='Subregion division strategy', verbose_name='Subregion division', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='subregion_selection',
            field=models.CharField(max_length=255, help_text='Strategy how subregion is selected for division', verbose_name='Subregion selection strategy', null=True),
        ),
    ]
