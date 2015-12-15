# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151215_1531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='algorithm',
            new_name='algorithm_title',
        ),
    ]
