# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150815_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='feed_id',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
