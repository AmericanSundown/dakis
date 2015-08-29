# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150825_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='branch',
            field=models.CharField(verbose_name='Branch', max_length=255, null=True, help_text='Branch of source code repository, need only if its not master branch'),
        ),
    ]
