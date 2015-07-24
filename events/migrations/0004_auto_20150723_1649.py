# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0003_auto_20150715_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='detail_group',
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(to='auth.Group', null=True, verbose_name='Group', blank=True),
        ),
    ]
