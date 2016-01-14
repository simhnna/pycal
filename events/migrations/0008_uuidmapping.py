# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160114_0218'),
    ]

    operations = [
        migrations.CreateModel(
            name='UUIDMapping',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False, editable=False, default=uuid.uuid4)),
                ('mapped_string', models.CharField(unique=True, db_index=True, max_length=120)),
            ],
        ),
    ]
