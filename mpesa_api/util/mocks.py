SUCCESS_B2C_SEND_RESPONSE = {
    "requestId": "4801-1149222-1",
    "ConversationID": "﻿AG_20171106_00004a65b655b9f47b4e",
    "OriginatorConversationID": "Service is currently under maintenance. Please try again later",
    "ResponseCode": "0",
    "ResponseDescription": "﻿The service request has been accepted successfully.",
}
SUCCESS_TOKEN_REQUEST = {
    "access_token": "ugqniOdaIapbTs8AkGPZPGHmRzjm",
    "expires_in": "3599",
}
FAILED_B2C_SEND_RESPONSE = {
    "errorCode": "500.002.1001",
    "errorMessage": "Service is currently under maintenance. Please try again later",
    "requestId": "8953-1200747-1",
}

B2C_SUCCESSFUL_RESULT = {
    "Result": {
        "ResultType": 0,
        "ResultCode": 0,
        "ResultDesc": "The service request has been accepted successfully.",
        "OriginatorConversationID": "19455-424535-1",
        "ConversationID": "AG_20170717_00006be9c8b5cc46abb6",
        "TransactionID": "LGH3197RIB",
        "ResultParameters": {
            "ResultParameter": [
                {"Key": "TransactionReceipt", "Value": "LGH3197RIB"},
                {"Key": "TransactionAmount", "Value": 8000},
                {"Key": "B2CWorkingAccountAvailableFunds", "Value": 150000},
                {"Key": "B2CUtilityAccountAvailableFunds", "Value": 133568},
                {
                    "Key": "TransactionCompletedDateTime",
                    "Value": "17.07.2017 10:54:57",
                },
                {
                    "Key": "ReceiverPartyPublicName",
                    "Value": "254708374149 - John Doe",
                },
                {"Key": "B2CChargesPaidAccountAvailableFunds", "Value": 0},
                {"Key": "B2CRecipientIsRegisteredCustomer", "Value": "Y"},
            ]
        },
        "ReferenceData": {
            "ReferenceItem": {
                "Key": "QueueTimeoutURL",
                "Value": "https://internalsandbox.safaricom.co.ke/mpesa/b2cresults/v1/submit",
            }
        },
    }
}

REGISTER_URL_SUCCESS = {
    "ConversationID": "",
    "OriginatorCoversationID": "",
    "ResponseDescription": "success",
}

ONLINE_REQUEST_RESPONSE = {
    "CheckoutRequestID": "ws_CO_12112017210342725",
    "CustomerMessage": "Success. Request accepted for processing",
    "MerchantRequestID": "4799-1246731-1",
    "ResponseCode": "0",
    "ResponseDescription": "Success. Request accepted for processing",
}

ONLINE_SUCCESS_RESPONSE = {
    "Body": {
        "stkCallback": {
            "MerchantRequestID": "19465-780693-1",
            "CheckoutRequestID": "ws_CO_27072017154747416",
            "ResultCode": 0,
            "ResultDesc": "The service request is processed successfully.",
            "CallbackMetadata": {
                "Item": [
                    {"Name": "Amount", "Value": 1},
                    {"Name": "MpesaReceiptNumber", "Value": "LGR7OWQX0R"},
                    {"Name": "Balance"},
                    {"Name": "TransactionDate", "Value": 20170727154800},
                    {"Name": "PhoneNumber", "Value": 254721566839},
                ]
            },
        }
    }
}

PAYBILL_RESPONSE = {
    "TransactionType": "Pay Bill",
    "TransID": "LK631GQCSP",
    "TransTime": "20171106225323",
    "TransAmount": "100.00",
    "BusinessShortCode": "600000",
    "BillRefNumber": "Test",
    "InvoiceNumber": "",
    "OrgAccountBalance": "",
    "ThirdPartyTransID": "",
    "MSISDN": "254708374149",
    "FirstName": "John",
    "MiddleName": "J.",
    "LastName": "Doe",
}
