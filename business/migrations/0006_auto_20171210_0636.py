# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-10 06:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_salesinvoiceline_salesinvoice'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SalesInvoiceLine',
            new_name='SalesInvoiceLineMod',
        ),
        migrations.RenameModel(
            old_name='SalesInvoice',
            new_name='SalesInvoiceMod',
        ),
    ]
