# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import json_field.fields
import django_extensions.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20151122_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('title', models.CharField(help_text='Unique verbose name of this algorithm', max_length=255, null=True, verbose_name='Algorithm title')),
                ('description', models.TextField(help_text='This algorithm description', null=True, verbose_name='Description')),
                ('repository', models.CharField(help_text='Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis', max_length=255, null=True, verbose_name='Source code repository')),
                ('branch', models.CharField(help_text='Branch of source code repository, need only if its not master branch', max_length=255, null=True, verbose_name='Branch')),
                ('executable', models.CharField(help_text='Executable file in source code repository, e.g. main.out', max_length=255, null=True, verbose_name='Executable')),
                ('details', json_field.fields.JSONField(help_text='Algorithm details in JSON format', default='', null=True, verbose_name='Algorithm details')),
                ('is_major', models.BooleanField(default=False, help_text='Is this algorithm unique? And should it be used for comparison as its algorithm class representative?', verbose_name='Is major')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(null=True, blank=True, related_name='children', to='core.Algorithm')),
            ],
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='max_duration',
        ),
    ]
