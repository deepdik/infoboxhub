# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-04 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20180703_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloggerprofile',
            name='about',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]