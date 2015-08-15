# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activation_id',
            field=models.CharField(blank=True, null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='feed_id',
            field=models.CharField(max_length=64),
        ),
    ]
