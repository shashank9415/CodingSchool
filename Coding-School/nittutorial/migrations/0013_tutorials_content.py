# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nittutorial', '0012_remove_tutorials_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorials',
            name='content',
            field=models.TextField(default='abc'),
        ),
    ]
