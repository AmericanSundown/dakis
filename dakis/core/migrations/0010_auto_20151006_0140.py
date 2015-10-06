# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150907_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='details',
            field=json_field.fields.JSONField(verbose_name='Algorithm details', null=True, help_text='Algorithm details in JSON format', default=''),
        ),
        migrations.AddField(
            model_name='task',
            name='details',
            field=json_field.fields.JSONField(verbose_name='Task details', null=True, help_text='Task execution details in JSON format', default=''),
        ),
    ]
