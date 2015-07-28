# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_feed_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activation_id',
            field=models.CharField(blank=True, unique=True, null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='feed_id',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
