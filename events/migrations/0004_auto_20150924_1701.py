# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_attendant'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='all_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End', blank=True),
        ),
    ]
