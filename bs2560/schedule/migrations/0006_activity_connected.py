# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_remove_activity_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='connected',
            field=models.BooleanField(default=False),
        ),
    ]
