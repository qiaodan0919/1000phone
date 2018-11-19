# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-22 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('_password', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=32, unique=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('permission', models.IntegerField(default=0)),
            ],
        ),
    ]