class MpesaBaseError(ValueError):
    """Loan Base Error"""

    pass


class B2CMpesaError(MpesaBaseError):
    """B2c Error"""

    pass


class C2BMpesaError(MpesaBaseError):
    """C2B Error"""

    pass


class StkPushMpesaError(MpesaBaseError):
    """Stk Push Error"""

    pass


class UrlRegisterMpesaError(MpesaBaseError):
    """C2B Error"""

    pass
