# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mpesa_core", "0012_onlinecheckout_transaction_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="B2CResponse",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("phone", models.BigIntegerField(blank=True, null=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "conversation_id",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "originator_conversation_id",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "result_type",
                    models.CharField(blank=True, max_length=5, null=True),
                ),
                (
                    "result_code",
                    models.CharField(blank=True, max_length=5, null=True),
                ),
                (
                    "result_description",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "transaction_receipt",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "transaction_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "working_funds",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "utility_funds",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "paid_account_funds",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "mpesa_user_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "is_registered_customer",
                    models.CharField(blank=True, max_length=1, null=True),
                ),
            ],
            options={
                "verbose_name_plural": "B2C Responses",
                "db_table": "tbl_b2c_response",
            },
        ),
        migrations.CreateModel(
            name="OnlineCheckoutResponse",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "merchant_request_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "checkout_request_id",
                    models.CharField(default="", max_length=50),
                ),
                (
                    "result_code",
                    models.CharField(blank=True, max_length=5, null=True),
                ),
                (
                    "result_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "mpesa_receipt_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "transaction_date",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("phone", models.BigIntegerField(blank=True, null=True)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Online Checkout Responses",
                "db_table": "tbl_online_checkout_responses",
            },
        ),
        migrations.AlterModelOptions(
            name="onlinecheckout",
            options={"verbose_name_plural": "Online Checkout Requests"},
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="is_registered_customer",
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="mpesa_user_name",
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="paid_account_funds",
        ),
        migrations.RemoveField(model_name="b2crequest", name="result_code",),
        migrations.RemoveField(
            model_name="b2crequest", name="result_description",
        ),
        migrations.RemoveField(model_name="b2crequest", name="result_type",),
        migrations.RemoveField(
            model_name="b2crequest", name="transaction_amount",
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="transaction_date",
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="transaction_id",
        ),
        migrations.RemoveField(
            model_name="b2crequest", name="transaction_receipt",
        ),
        migrations.RemoveField(model_name="b2crequest", name="utility_funds",),
        migrations.RemoveField(model_name="b2crequest", name="working_funds",),
        migrations.RemoveField(
            model_name="onlinecheckout", name="mpesa_receipt_number",
        ),
        migrations.RemoveField(
            model_name="onlinecheckout", name="result_code",
        ),
        migrations.RemoveField(
            model_name="onlinecheckout", name="result_description",
        ),
        migrations.RemoveField(
            model_name="onlinecheckout", name="transaction_date",
        ),
    ]
