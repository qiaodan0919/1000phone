# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-12 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='u_name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]