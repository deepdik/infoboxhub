# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-20 18:13
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0043_bloggerprofile_image_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpictures',
            name='image_10',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.upload_location_pic),
        ),
        migrations.AddField(
            model_name='postpictures',
            name='image_8',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.upload_location_pic),
        ),
        migrations.AddField(
            model_name='postpictures',
            name='image_9',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.upload_location_pic),
        ),
    ]
