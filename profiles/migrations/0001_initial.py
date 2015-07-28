# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('activation_id', models.CharField(max_length=64, unique=True, null=True, blank=True)),
                ('email_notifications', models.BooleanField(default=False)),
                ('unverified_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('feed_id', models.CharField(max_length=64, unique=True)),
            ],
        ),
    ]
