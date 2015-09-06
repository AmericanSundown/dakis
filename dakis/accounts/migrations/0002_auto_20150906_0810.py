# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='host_password',
            field=models.CharField(max_length=255, blank=True, default='', verbose_name='Host password'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='hostname',
            field=models.CharField(max_length=255, blank=True, default='', verbose_name='Hostname of computing resourses'),
        ),
    ]
