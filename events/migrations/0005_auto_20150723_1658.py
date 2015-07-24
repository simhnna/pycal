# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150723_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=50),
        ),
    ]
