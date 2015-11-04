# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_experiment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False),
        ),
        migrations.AddField(
            model_name='task',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False),
        ),
    ]
