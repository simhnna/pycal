# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150707_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('start_date', models.DateTimeField(verbose_name='Start')),
                ('end_date', models.DateTimeField(null=True, blank=True, verbose_name='End')),
                ('title', models.CharField(max_length=16, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('created_by', models.ForeignKey(to='profiles.Profile')),
            ],
        ),
    ]
