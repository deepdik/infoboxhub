# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-09-24 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0049_category_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='keywords',
            new_name='url_keyword',
        ),
    ]
