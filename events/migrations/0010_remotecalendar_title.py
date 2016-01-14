# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_remotecalendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotecalendar',
            name='title',
            field=models.CharField(max_length=60, default='Baustelle'),
            preserve_default=False,
        ),
    ]
