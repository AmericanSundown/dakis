# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenIDNonce',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenIDStore',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.TextField()),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='socialaccount',
            name='provider',
            field=models.CharField(choices=[('google', 'Google'), ('github', 'GitHub'), ('openid', 'OpenID'), ('persona', 'Persona')], max_length=30, verbose_name='provider'),
        ),
        migrations.AlterField(
            model_name='socialapp',
            name='provider',
            field=models.CharField(choices=[('google', 'Google'), ('github', 'GitHub'), ('persona', 'Persona')], max_length=30, verbose_name='provider'),
        ),
    ]
