# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150824_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='executable',
            field=models.CharField(max_length=255, null=True, help_text='Executable file in source code repository, e.g. main.out', verbose_name='Executable'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='source_code_repository',
            field=models.CharField(max_length=255, null=True, help_text='Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis', verbose_name='Source code repository'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='algorithm',
            field=models.CharField(max_length=255, null=True, help_text='Unique verbose name of this algorithm', verbose_name='Algorithm'),
        ),
    ]
