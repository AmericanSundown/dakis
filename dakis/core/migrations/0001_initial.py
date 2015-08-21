# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                ('description', models.TextField(help_text='This experiment description', verbose_name='Description', null=True)),
                ('algorithm', models.CharField(help_text='Name of algorithm', max_length=255, verbose_name='Algorithm', null=True)),
                ('neighbours', models.CharField(help_text='Strategy how neighbours are determined', max_length=255, verbose_name='Neighbours', null=True)),
                ('stopping_criteria', models.CharField(help_text='Stopping criteria strategy', max_length=255, verbose_name='Stopping criteria', null=True)),
                ('stopping_accuracy', models.CharField(help_text='Stopping accuracy', max_length=255, verbose_name='Stopping accuracy', null=True)),
                ('subregion', models.CharField(help_text='Subregion type: simplex or rectangle', max_length=255, verbose_name='Subregion', null=True)),
                ('inner_problem_accuracy', models.CharField(help_text='Inner problem solution accuracy', max_length=255, verbose_name='Inner accuracy', null=True)),
                ('inner_problem_iters', models.IntegerField(help_text='Inner problem maximum iterations to get solution', verbose_name='Inner iters', null=True)),
                ('inner_problem_division', models.CharField(help_text='Inner problem subregion division strategy', max_length=255, verbose_name='Division strategy in inner problem', null=True)),
                ('lipschitz_estimation', models.CharField(help_text='Subregion Lipschitz constant estimation strategy', max_length=255, verbose_name='Lipschitz estimation', null=True)),
                ('simplex_division', models.CharField(help_text='Subregion division strategy', max_length=255, verbose_name='Simplex division', null=True)),
                ('valid', models.BooleanField(default=True, help_text='Is this experiment valid? Its not valid if critical mistake was found.', verbose_name='Valid')),
                ('mistakes', models.TextField(help_text='Descriptions of mistakes, which were found in this experiment', verbose_name='Mistakes', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('func_name', models.CharField(help_text='Function name', max_length=255, verbose_name='Function name', null=True)),
                ('func_cls', models.IntegerField(help_text='GKLS function class', verbose_name='GKLS class', null=True)),
                ('func_id', models.IntegerField(help_text='GKLS function id', verbose_name='GKLS id', null=True)),
                ('calls', models.IntegerField(help_text='Calls', verbose_name='Calls', null=True)),
                ('subregions', models.IntegerField(help_text='Subregions in final partition', verbose_name='Subregions', null=True)),
                ('duration', models.DurationField(help_text='Duration of task execution', verbose_name='Duration', null=True)),
                ('f_min', models.FloatField(help_text='Value of minimum, which managed to determine', verbose_name='F min', null=True)),
                ('x_min', models.CharField(help_text='Determined minimum coordinates', max_length=255, verbose_name='X min', null=True)),
                ('experiment', models.ForeignKey(related_name='tasks', help_text='ID of experiment to which this task is assigned to', null=True, to='core.Experiment')),
            ],
        ),
    ]
