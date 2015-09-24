# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150924_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='feed_id',
            field=models.CharField(null=True, max_length=64, unique=True, blank=True),
        ),
    ]
