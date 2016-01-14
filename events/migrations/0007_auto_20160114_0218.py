# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import uuid
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150924_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 14, 1, 18, 12, 382121, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 14, 1, 18, 20, 973714, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(db_index=True, editable=False, default=uuid.uuid4),
        ),
    ]
