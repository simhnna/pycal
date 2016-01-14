# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_remotecalendar_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='remotecalendar',
            old_name='Category',
            new_name='category',
        ),
    ]
