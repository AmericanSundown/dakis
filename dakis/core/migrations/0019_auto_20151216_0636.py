# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import json_field.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151216_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='Problem title', help_text='Unique verbose name of this problem', null=True)),
                ('input_params', json_field.fields.JSONField(default='', verbose_name='Input parameters', help_text='Parameters for each experiment task. Ranges available, e.g. 1..10. Nesting available.', null=True)),
                ('output_params', json_field.fields.JSONField(default='', verbose_name='Output parameters', help_text='Enter a valid JSON object', null=True)),
                ('description', models.TextField(verbose_name='Description', help_text='Problem description', null=True)),
                ('parent', models.ForeignKey(to='core.Problem', null=True, related_name='children', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='experiment',
            name='algorithm',
            field=models.ForeignKey(to='core.Algorithm', null=True, help_text='Algorithm which is used for this experiment'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='problem',
            field=models.ForeignKey(to='core.Problem', null=True, help_text='Problem which is solved in this experiment'),
        ),
    ]
