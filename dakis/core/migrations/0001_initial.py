# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('description', models.TextField(verbose_name='Description', null=True, help_text='This experiment description')),
                ('algorithm', models.CharField(verbose_name='Algorithm', null=True, help_text='Name of algorithm', max_length=255)),
                ('neighbours', models.CharField(verbose_name='Neighbours', null=True, help_text='Strategy how neighbours are determined', max_length=255)),
                ('stopping_criteria', models.CharField(verbose_name='Stopping criteria', null=True, help_text='Stopping criteria strategy', max_length=255)),
                ('stopping_accuracy', models.CharField(verbose_name='Stopping accuracy', null=True, help_text='Stopping accuracy', max_length=255)),
                ('subregion', models.CharField(verbose_name='Subregion', null=True, help_text='Subregion type: simplex or rectangle', max_length=255)),
                ('inner_problem_accuracy', models.CharField(verbose_name='Inner accuracy', null=True, help_text='Inner problem solution accuracy', max_length=255)),
                ('inner_problem_iters', models.IntegerField(verbose_name='Inner iters', null=True, help_text='Inner problem maximum iterations to get solution')),
                ('inner_problem_division', models.CharField(verbose_name='Division strategy in inner problem', null=True, help_text='Inner problem subregion division strategy', max_length=255)),
                ('lipschitz_estimation', models.CharField(verbose_name='Lipschitz estimation', null=True, help_text='Subregion Lipschitz constant estimation strategy', max_length=255)),
                ('simplex_division', models.CharField(verbose_name='Simplex division', null=True, help_text='Subregion division strategy', max_length=255)),
                ('invalid', models.BooleanField(verbose_name='Not valid', default=True, help_text='Is this experiment not valid? Its not valid if critical mistake was found.')),
                ('mistakes', models.TextField(verbose_name='Mistakes', null=True, help_text='Descriptions of mistakes, which were found in this experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('func_name', models.CharField(verbose_name='Function name', null=True, help_text='Function name', max_length=255)),
                ('func_cls', models.IntegerField(verbose_name='GKLS class', null=True, help_text='GKLS function class')),
                ('func_id', models.IntegerField(verbose_name='GKLS id', null=True, help_text='GKLS function id')),
                ('calls', models.IntegerField(verbose_name='Calls', null=True, help_text='Calls')),
                ('subregions', models.IntegerField(verbose_name='Subregions', null=True, help_text='Subregions in final partition')),
                ('duration', models.FloatField(verbose_name='Duration', null=True, help_text='Task execution duration in seconds')),
                ('f_min', models.FloatField(verbose_name='F min', null=True, help_text='Value of minimum, which managed to determine')),
                ('x_min', models.CharField(verbose_name='X min', null=True, help_text='Determined minimum coordinates', max_length=255)),
                ('status', models.CharField(verbose_name='Status', default='C', choices=[('C', 'Created'), ('R', 'Running'), ('S', 'Suspended'), ('D', 'Done')], max_length=2)),
                ('experiment', models.ForeignKey(related_name='tasks', help_text='ID of experiment to which this task is assigned to', null=True, to='core.Experiment')),
            ],
        ),
    ]
