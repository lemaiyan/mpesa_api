from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from mpesa_api.core.models import (
    B2CRequest,
    B2CResponse,
    C2BRequest,
    OnlineCheckout,
    OnlineCheckoutResponse,
)


@admin.register(B2CRequest)
class B2CRequestAdmin(admin.ModelAdmin):
    list_display = ("phone", "amount")
    readonly_fields = (
        "phone",
        "amount",
        "conversation_id",
        "originator_conversation_id",
        "response_code",
        "response_description",
        "request_id",
        "error_code",
        "error_message",
        "date_added",
    )
    search_fields = ("phone",)
    list_filter = (("date_added", DateRangeFilter),)


@admin.register(B2CResponse)
class B2CResponseAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "amount",
        "transaction_receipt",
        "mpesa_user_name",
    )
    readonly_fields = (
        "phone",
        "amount",
        "conversation_id",
        "originator_conversation_id",
        "result_type",
        "result_code",
        "result_description",
        "transaction_id",
        "transaction_receipt",
        "transaction_amount",
        "working_funds",
        "utility_funds",
        "paid_account_funds",
        "transaction_date",
        "mpesa_user_name",
        "is_registered_customer",
    )
    search_fields = ("phone", "transaction_receipt", "mpesa_user_name")
    list_filter = (("transaction_date", DateRangeFilter),)


@admin.register(C2BRequest)
class C2BRequestAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "amount",
        "name",
        "transaction_id",
        "transaction_date",
    )
    readonly_fields = (
        "phone",
        "amount",
        "name",
        "transaction_id",
        "transaction_date",
        "business_short_code",
        "bill_ref_number",
        "invoice_number",
        "org_account_balance",
        "third_party_trans_id",
        "is_validated",
        "is_completed",
        "date_added",
    )
    search_fields = ("phone", "transaction_id", "name")
    list_filter = (
        ("transaction_date", DateRangeFilter),
        ("date_added", DateRangeFilter),
    )


@admin.register(OnlineCheckout)
class OnlineCheckoutAdmin(admin.ModelAdmin):
    list_display = ("phone", "amount", "date_added")
    readonly_fields = (
        "phone",
        "amount",
        "checkout_request_id",
        "account_reference",
        "transaction_description",
        "customer_message",
        "merchant_request_id",
        "response_code",
        "response_description",
        "date_added",
    )
    search_fields = ("phone", "amount", "date_added")
    list_filter = (("date_added", DateRangeFilter),)


@admin.register(OnlineCheckoutResponse)
class OnlineCheckoutResponseAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "amount",
        "mpesa_receipt_number",
        "transaction_date",
    )
    readonly_fields = (
        "phone",
        "amount",
        "transaction_date",
        "mpesa_receipt_number",
        "result_description",
        "result_code",
        "checkout_request_id",
        "merchant_request_id",
        "date_added",
    )
    search_fields = ("phone", "amount", "date_added", "mpesa_receipt_number")
    list_filter = (
        ("transaction_date", DateRangeFilter),
        ("date_added", DateRangeFilter),
    )
