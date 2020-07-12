from django.urls import path

from mpesa_api.core.views import (
    B2cResult,
    B2cTimeOut,
    C2bConfirmation,
    C2bValidation,
    OnlineCheckoutCallback,
)

app_name = "mpesa"

urlpatterns = [
    path("b2c/timeout", B2cTimeOut.as_view(), name="b2c_timeout"),
    path("b2c/result", B2cResult.as_view(), name="b2c_result"),
    path(
        "c2b/confirmation", C2bConfirmation.as_view(), name="c2b_confirmation"
    ),
    path("c2b/validate", C2bValidation.as_view(), name="c2b_validation"),
    path(
        "c2b/online_checkout/callback",
        OnlineCheckoutCallback.as_view(),
        name="c2b_checkout_callback",
    ),
]
