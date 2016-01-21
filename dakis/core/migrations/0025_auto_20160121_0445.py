# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_task_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='algorithm',
            old_name='parent',
            new_name='algorithm_parent',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='parent',
            new_name='problem_parent',
        ),
        migrations.RenameField(
            model_name='algorithm',
            old_name='description',
            new_name='algorithm_description',
        ),
        migrations.RenameField(
            model_name='algorithm',
            old_name='title',
            new_name='algorithm_title',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='description',
            new_name='problem_description',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='title',
            new_name='problem_title',
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='branch',
            field=models.CharField(verbose_name='Branch', max_length=255, blank=True, help_text='Branch of source code repository, need only if its not master branch', null=True),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='details',
            field=json_field.fields.JSONField(verbose_name='Algorithm details', blank=True, help_text='Algorithm details in JSON format', null=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='executable',
            field=models.CharField(verbose_name='Executable', max_length=255, blank=True, help_text='Executable file in source code repository, e.g. main.out', null=True),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='repository',
            field=models.CharField(verbose_name='Source code repository', max_length=255, blank=True, help_text='Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis', null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True, help_text='This experiment description', null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='mistakes',
            field=models.TextField(verbose_name='Mistakes', blank=True, help_text='Descriptions of mistakes, which were found in this experiment', null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='input_params',
            field=json_field.fields.JSONField(verbose_name='Input parameters', blank=True, help_text='Parameters for each experiment task. Ranges available, e.g. 1..10. Nesting available.', null=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='result_display_params',
            field=json_field.fields.JSONField(verbose_name='Result display discribing parameters', blank=True, help_text='Enter a valid JSON object', null=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='task',
            name='input_values',
            field=json_field.fields.JSONField(verbose_name='Input parameters', help_text='Parameters for each experiment task.', null=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='task',
            name='output_values',
            field=json_field.fields.JSONField(verbose_name='Output parameters', help_text='Enter a valid JSON object', null=True, default='[]'),
        ),
    ]
