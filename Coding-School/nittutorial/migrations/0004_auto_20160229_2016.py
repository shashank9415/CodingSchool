# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 14:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nittutorial', '0003_auto_20160229_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorials',
            name='contentId',
            field=models.ForeignKey(db_column='contentId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nittutorial.Content', unique=True),
        ),
    ]
