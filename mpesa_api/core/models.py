from django.db import models

from mpesa_api.util.managers import AuthTokenManager


class AuthToken(models.Model):
    """Handles AuthTokens"""

    access_token = models.CharField(max_length=40)
    type = models.CharField(max_length=3)
    expires_in = models.BigIntegerField()
    objects = AuthTokenManager()

    def __str__(self):
        return self.access_token

    class Meta:
        db_table = "tbl_access_token"


class B2CRequest(models.Model):
    """
    Handles B2C requests
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    conversation_id = models.CharField(max_length=40, blank=True, null=True)
    originator_conversation_id = models.CharField(
        max_length=40, blank=True, null=True
    )
    response_code = models.CharField(max_length=5, blank=True, null=True)
    response_description = models.TextField(blank=True, null=True)
    request_id = models.CharField(max_length=20, blank=True, null=True)
    error_code = models.CharField(max_length=20, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_b2c_requests"
        verbose_name_plural = "B2C Requests"


class B2CResponse(models.Model):
    """
    Handles B2C Response
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    conversation_id = models.CharField(max_length=40, blank=True, null=True)
    originator_conversation_id = models.CharField(
        max_length=40, blank=True, null=True
    )
    result_type = models.CharField(max_length=5, blank=True, null=True)
    result_code = models.CharField(max_length=5, blank=True, null=True)
    result_description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    transaction_receipt = models.CharField(
        max_length=20, blank=True, null=True
    )
    transaction_amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    working_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    utility_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    paid_account_funds = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    transaction_date = models.DateTimeField(blank=True, null=True)
    mpesa_user_name = models.CharField(max_length=100, blank=True, null=True)
    is_registered_customer = models.CharField(
        max_length=1, blank=True, null=True
    )

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_b2c_response"
        verbose_name_plural = "B2C Responses"


class C2BRequest(models.Model):
    """
    Handles C2B Requests
    """

    id = models.BigAutoField(primary_key=True)
    transaction_type = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=20, unique=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    business_short_code = models.CharField(
        max_length=20, blank=True, null=True
    )
    bill_ref_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    org_account_balance = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, default=0.0
    )
    third_party_trans_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    phone = models.BigIntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_validated = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(
            self.first_name, self.middle_name, self.last_name
        )

    class Meta:
        db_table = "tbl_c2b_requests"
        verbose_name_plural = "C2B Requests"

    @property
    def name(self):
        return "{} {} {}".format(
            self.first_name, self.middle_name, self.last_name
        )


class OnlineCheckout(models.Model):
    """
    Handles Online Checkout
    """

    id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    is_paybill = models.BooleanField(default=True)
    checkout_request_id = models.CharField(max_length=50, default="")
    account_reference = models.CharField(max_length=50, default="")
    transaction_description = models.CharField(
        max_length=50, blank=True, null=True
    )
    customer_message = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    response_code = models.CharField(max_length=5, blank=True, null=True)
    response_description = models.CharField(
        max_length=100, blank=True, null=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_online_checkout_requests"
        verbose_name_plural = "Online Checkout Requests"


class OnlineCheckoutResponse(models.Model):
    """
    Handles Online Checkout Response
    """

    id = models.BigAutoField(primary_key=True)
    merchant_request_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    checkout_request_id = models.CharField(max_length=50, default="")
    result_code = models.CharField(max_length=5, blank=True, null=True)
    result_description = models.CharField(
        max_length=100, blank=True, null=True
    )
    mpesa_receipt_number = models.CharField(
        max_length=50, blank=True, null=True
    )
    transaction_date = models.DateTimeField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone)

    class Meta:
        db_table = "tbl_online_checkout_responses"
        verbose_name_plural = "Online Checkout Responses"
