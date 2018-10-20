# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part_1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CustomerKey', models.CharField(max_length=100)),
                ('CustomerSecretKey', models.CharField(max_length=100)),
                ('AccessTokenKey', models.CharField(max_length=100)),
                ('AccessTokenSecret', models.CharField(max_length=100)),
            ],
        ),
    ]
