# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-07 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountingbuddy', '0011_auto_20171024_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Enter HTML Content')),
            ],
        ),
    ]