# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-09-24 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0047_auto_20230924_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='svg_class',
            field=models.CharField(blank=True, max_length=39, null=True),
        ),
    ]
