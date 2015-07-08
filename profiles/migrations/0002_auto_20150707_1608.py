# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activation_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email_notifications',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='unverified_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
