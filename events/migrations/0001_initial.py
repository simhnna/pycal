# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start_date', models.DateTimeField(verbose_name='Start')),
                ('end_date', models.DateTimeField(verbose_name='End', null=True, blank=True)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('details', models.TextField(verbose_name='Details', null=True, blank=True)),
                ('group', models.ForeignKey(verbose_name='Group', blank=True, to='auth.Group', null=True)),
            ],
        ),
    ]
