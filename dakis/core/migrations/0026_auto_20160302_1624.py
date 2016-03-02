# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20160121_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='algorithm_description',
            field=models.TextField(verbose_name='Description', blank=True, null=True, help_text='This algorithm description'),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='algorithm_title',
            field=models.CharField(verbose_name='Algorithm title', blank=True, max_length=255, null=True, help_text='Unique verbose name of this algorithm'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='threads',
            field=models.IntegerField(verbose_name='Threads', default=0, help_text='How many threads are currently running'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='problem_description',
            field=models.TextField(verbose_name='Description', blank=True, null=True, help_text='Problem description'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='problem_title',
            field=models.CharField(verbose_name='Problem title', blank=True, max_length=255, null=True, help_text='Unique verbose name of this problem'),
        ),
    ]
