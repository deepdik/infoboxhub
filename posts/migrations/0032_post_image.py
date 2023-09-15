# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-09 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0031_auto_20180709_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=1, height_field='height_field', upload_to=posts.models.upload_location, width_field='width_field'),
            preserve_default=False,
        ),
    ]
