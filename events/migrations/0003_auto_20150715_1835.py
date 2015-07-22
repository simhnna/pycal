# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0002_auto_20150714_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='detail_group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='details',
            field=models.TextField(null=True, verbose_name='Details', blank=True),
        ),
    ]
