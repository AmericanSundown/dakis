# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20151231_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='output_params',
        ),
        migrations.AddField(
            model_name='problem',
            name='result_display_params',
            field=json_field.fields.JSONField(help_text='Enter a valid JSON object', null=True, verbose_name='Result display discribing parameters', default=''),
        ),
    ]
