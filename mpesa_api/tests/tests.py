from django.test import TestCase, override_settings, Client
import requests
from unittest import mock
from django.conf import settings
from mpesa_api.util.mpesautils import get_token
from mpesa_api.core.models import B2CRequest, OnlineCheckout
from mpesa_api.core.mpesa import Mpesa
from mpesa_api.core import tasks
from mpesa_api.util import mocks
from mpesa_api.util.b2cutils import send_b2c_request
from mpesa_api.util.c2butils import register_c2b_url, process_online_checkout
from django.urls import reverse
from mpesa_api.core import signals
from django.db.models.signals import post_save
from mpesa_api.core.tasks import (
    process_b2c_call_response_task,
    send_b2c_request_task,
    call_online_checkout_task,
    handle_online_checkout_response_task,
)
from celery import chain


class MockResponse:
    """
    MockResponse Class
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_requests_get(*args, **kwargs):
    """
    Mock requests get
    :param args:
    :param kwargs:
    :return:
    """
    url = kwargs["url"]
    if url == f"{settings.MPESA_URL}/oauth/v1/generate?grant_type=client_credentials":
        return MockResponse(mocks.SUCCESS_TOKEN_REQUEST, 200)


def mock_requests_post(*args, **kwargs):
    """
    Mock requests post
    :param args:
    :param kwargs:
    :return:
    """
    url = kwargs["url"]
    if url == f"{settings.MPESA_URL}/mpesa/b2c/v1/paymentrequest":
        return MockResponse(mocks.SUCCESS_B2C_SEND_RESPONSE, 200)
    elif url == f"{settings.MPESA_URL}/mpesa/c2b/v1/registerurl":
        return MockResponse(mocks.REGISTER_URL_SUCCESS, 200)
    elif url == f"{settings.MPESA_URL}/mpesa/stkpush/v1/processrequest":
        return MockResponse(mocks.ONLINE_REQUEST_RESPONSE, 200)


def post(url, data):
    c = Client()
    response = c.post(url, data)
    return response.content.decode("utf-8")


class FetchTokenTest(TestCase):
    """
    Fetch Token Test
    """

    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_token_is_fetched_as_expected(self, mock_get):
        response = get_token("c2b")
        self.assertEqual(response, mocks.SUCCESS_TOKEN_REQUEST)
        self.assertTrue(mock_get.called)


@mock.patch("requests.get", side_effect=mock_requests_get)
@mock.patch("requests.post", side_effect=mock_requests_post)
@override_settings(CELERY_ALWAYS_EAGER=True)
class B2CMethodsTest(TestCase):
    def setUp(self):
        self.req = Mpesa.b2c_request(phone=254708374149, amount=100.0)

    def test_successful_b2c_request(self, mock_post, mock_get):
        response = send_b2c_request(
            int(self.req.amount), self.req.phone, self.req.id
        )
        self.assertEqual(response, mocks.SUCCESS_B2C_SEND_RESPONSE)
        self.assertTrue(mock_post.called)

    def test_failed_b2c_request(self, mock_post, mock_get):
        response = send_b2c_request(
            int(self.req.amount), self.req.phone, self.req.id
        )
        response = mocks.FAILED_B2C_SEND_RESPONSE
        self.assertEqual(response, mocks.FAILED_B2C_SEND_RESPONSE)
        self.assertTrue(mock_post.called)

    def test_b2c_result_url(self, mock_post, mock_get):
        url = reverse("mpesa:b2c_result")
        response = post(url, mocks.B2C_SUCCESSFUL_RESULT)
        self.assertEqual(
            '{"value":"ok","key":"status","detail":"success"}', response
        )

    def test_b2c_timeout_url(self, mock_post, mock_get):
        url = reverse("mpesa:b2c_timeout")
        response = post(url, mocks.B2C_SUCCESSFUL_RESULT)
        self.assertEqual(
            '{"value":"ok","key":"status","detail":"success"}', response
        )

    @mock.patch(
        "mpesa_api.core.signals.handle_b2c_request_post_save", autospec=True
    )
    def test_b2c__post_save_signal(self, mock_signal, mock_post, mock_get):
        post_save.connect(
            mock_signal,
            sender=B2CRequest,
            dispatch_uid="test_b2c_request_post_save",
        )
        Mpesa.b2c_request(phone=254708374149, amount=100.0)
        self.assertEquals(mock_signal.call_count, 1)
        post_save.disconnect(
            mock_signal,
            sender=B2CRequest,
            dispatch_uid="test_b2c_request_post_save",
        )

    def test_b2c_tasks(self, mock_post, mock_get):
        self.assertTrue(
            chain(
                send_b2c_request_task.s(100, 254708374149, 1),
                process_b2c_call_response_task.s(1),
            ).apply_async()
        )

    def tearDown(self):
        post_save.connect(
            signals.handle_b2c_request_post_save, sender=B2CRequest
        )


@mock.patch("requests.get", side_effect=mock_requests_get)
@mock.patch("requests.post", side_effect=mock_requests_post)
@override_settings(CELERY_ALWAYS_EAGER=True)
class C2BMethodTest(TestCase):
    def test_register_c2b_url(self, mock_post, mock_get):
        response = Mpesa.c2b_register_url()
        self.assertEqual(mocks.REGISTER_URL_SUCCESS, response)

    def setUp(self):
        self.request = Mpesa.stk_push(
            phone=254708374149, amount=100.0, account_reference="Test"
        )

    def test_successful_online_checkout_response(self, mock_post, mock_get):
        resp = process_online_checkout(
            self.request.phone, int(self.request.amount), "Test", "test"
        )
        self.assertEqual(mocks.ONLINE_REQUEST_RESPONSE, resp)

    def test_success_online_checkout_url(self, mock_post, mock_get):
        url = reverse("mpesa:c2b_checkout_callback")
        response = post(url, mocks.ONLINE_SUCCESS_RESPONSE)
        self.assertEqual(
            '{"value":"ok","key":"status","detail":"success"}', response
        )

    def test_validation_url(self, mock_post, mock_get):
        url = reverse("mpesa:c2b_validation")
        response = post(url, mocks.PAYBILL_RESPONSE)
        self.assertEqual(
            '{"value":"ok","key":"status","detail":"success"}', response
        )

    def test_confirmation_url(self, mock_post, mock_get):
        url = reverse("mpesa:c2b_confirmation")
        response = post(url, mocks.PAYBILL_RESPONSE)
        self.assertEqual(
            '{"value":"ok","key":"status","detail":"success"}', response
        )

    @mock.patch(
        "mpesa_api.core.signals.handle_online_checkout_post_save",
        autospec=True,
    )
    def test_c2b_post_save_signal(self, mock_signal, mock_post, mock_get):
        post_save.connect(
            mock_signal,
            sender=OnlineCheckout,
            dispatch_uid="test_online_request_post_save",
        )
        Mpesa.stk_push(
            phone=254708374149, amount=100.0, account_reference="Test"
        )
        self.assertEquals(mock_signal.call_count, 1)
        post_save.disconnect(
            mock_signal,
            sender=OnlineCheckout,
            dispatch_uid="test_online_request_post_save",
        )

    def test_online_tasks(self, mock_post, mock_get):
        self.assertTrue(
            chain(
                call_online_checkout_task.s(254708374149, 100, "", "", True),
                handle_online_checkout_response_task.s(1),
            ).apply_async()
        )

    def tearDown(self):
        post_save.connect(
            signals.handle_online_checkout_post_save, sender=OnlineCheckout
        )
