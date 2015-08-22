# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='valid',
        ),
        migrations.AddField(
            model_name='experiment',
            name='invalid',
            field=models.BooleanField(default=True, help_text='Is this experiment not valid? Its not valid if critical mistake was found.', verbose_name='Not valid'),
        ),
    ]
