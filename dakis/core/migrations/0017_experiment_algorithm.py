# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151215_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='algorithm',
            field=models.ForeignKey(null=True, help_text='Algorithm which is used for experiment', to='core.Algorithm'),
        ),
    ]
