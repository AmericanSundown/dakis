# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import concurrency.fields
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_problem_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='calls',
        ),
        migrations.RemoveField(
            model_name='task',
            name='details',
        ),
        migrations.RemoveField(
            model_name='task',
            name='f_min',
        ),
        migrations.RemoveField(
            model_name='task',
            name='func_cls',
        ),
        migrations.RemoveField(
            model_name='task',
            name='func_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='func_name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='subregions',
        ),
        migrations.RemoveField(
            model_name='task',
            name='x_min',
        ),
        migrations.AddField(
            model_name='task',
            name='input_values',
            field=json_field.fields.JSONField(help_text='Parameters for each experiment task.', verbose_name='Input parameters', default='', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='output_values',
            field=json_field.fields.JSONField(help_text='Enter a valid JSON object', verbose_name='Output parameters', default='', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='stderr',
            field=models.TextField(help_text='Standard error stream', verbose_name='stderr', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='stdout',
            field=models.TextField(help_text='Standard output stream', verbose_name='stdout', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='version',
            field=concurrency.fields.IntegerVersionField(help_text='record revision number', default=1),
        ),
    ]
