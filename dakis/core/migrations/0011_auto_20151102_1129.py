# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20151006_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='is_major',
            field=models.BooleanField(verbose_name='Is major', help_text='Is this algorithm unique? And should it be used for comparison as its algorithm class representative?', default=False),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='invalid',
            field=models.BooleanField(verbose_name='Not valid', help_text='Is this experiment not valid? Its not valid if critical mistake was found.', default=False),
        ),
    ]
