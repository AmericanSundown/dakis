# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150907_0317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='source_code_repository',
            new_name='repository',
        ),
    ]
