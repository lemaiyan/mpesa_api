# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mpesa_core", "0011_auto_20171108_2343"),
    ]

    operations = [
        migrations.AddField(
            model_name="onlinecheckout",
            name="transaction_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
