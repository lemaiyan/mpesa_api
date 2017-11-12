from django.test import TestCase, override_settings
import requests
from unittest import mock
from django.conf import settings
from mpesa_api.util.mpesautils import get_token
from mpesa_api.core.models import B2CRequest, AuthToken
from mpesa_api.core import tasks
from mpesa_api.util import mocks
from mpesa_api.util.b2cutils import send_b2c_request


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_requests_get(*args, **kwargs):
    url = kwargs['url']
    if url == settings.GENERATE_TOKEN_URL:
        return MockResponse(mocks.SUCCESS_TOKEN_REQUEST, 200)


def mock_requests_post(*args, **kwargs):
    url = kwargs['url']
    if url == settings.B2C_URL:
        return MockResponse(mocks.SUCCESS_B2C_SEND_RESPONSE, 200)


class FetchTokenTest(TestCase):
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_token_is_fetched_as_expected(self, mock_get):
        response = get_token()
        self.assertEqual(response, mocks.SUCCESS_TOKEN_REQUEST)
        self.assertTrue(mock_get.called)


@mock.patch('requests.get', side_effect=mock_requests_get)
@mock.patch('requests.post', side_effect=mock_requests_post)
@override_settings(CELERY_ALWAYS_EAGER=True)
class B2CMethodsTest(TestCase):
    def setUp(self):
        self.req = B2CRequest.objects.create(phone=254708374149, amount=100.0)

    def test_successful_b2c_request(self, mock_post, mock_get):
        response = send_b2c_request(int(self.req.amount), self.req.phone, self.req.id)
        self.assertEqual(response, mocks.SUCCESS_B2C_SEND_RESPONSE)
        self.assertTrue(mock_post.called)

    def test_failed_b2c_request(self, mock_post, mock_get):
        response = send_b2c_request(int(self.req.amount), self.req.phone, self.req.id)
        response = mocks.FAILED_B2C_SEND_RESPONSE
        self.assertEqual(response, mocks.FAILED_B2C_SEND_RESPONSE)
        self.assertTrue(mock_post.called)



