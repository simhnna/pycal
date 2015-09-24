# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150924_2021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories', 'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Events', 'verbose_name': 'Event'},
        ),
    ]
