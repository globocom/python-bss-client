import unittest
import mock

from bss_client import BSSClient
from bss_client.exception import BSSError


def mock_request(request_mock, status_code, return_value):
    response_obj = mock.Mock()
    response_obj.status_code = status_code
    response_obj.json = mock.Mock(return_value=return_value)
    response_obj.text = str(return_value)
    request_obj = mock.Mock()
    request_obj.request = mock.Mock(return_value=response_obj)
    request_mock.return_value = request_obj
    return request_obj


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = BSSClient("http://localhost", "xxx", "yyy", {
            'verify': False
        })

    def test_client(self):
        self.assertEqual(self.client.endpoint, "http://localhost")
        self.assertEqual(self.client.key, "xxx")
        self.assertEqual(self.client.secret, "yyy")
        self.assertDictEqual(self.client.requests_params, {
            'verify': False
        })

    def test_client_no_extra_args(self):
        client = BSSClient("http://localhost", "xxx", "yyy")
        self.assertDictEqual(client.requests_params, {})

    def test_client_create_request(self):
        req = self.client.create_request()
        self.assertEqual(req.endpoint, "http://localhost")
        self.assertEqual(req.key, "xxx")
        self.assertEqual(req.secret, "yyy")
        self.assertDictEqual(req.requests_params, {
            'headers': {'Content-Type': 'application/json'},
            'verify': False,
        })

    def test_handle_json_response(self):
        m = mock.Mock()
        m.status_code = 200
        m.json = mock.Mock(return_value=['val'])
        rsp = self.client._handle_json_response(m)
        self.assertEqual(rsp, ['val'])
        m2 = mock.Mock()
        m2.status_code = 500
        m2.text = 'someerror'
        with self.assertRaises(BSSError) as exc:
            self.client._handle_json_response(m2)
        self.assertEqual(exc.exception.code, 500)
        self.assertEqual(exc.exception.value, "someerror")
        self.assertEqual(str(exc.exception), '500 - someerror')

    @mock.patch("bss_client.client.Request")
    def test_list_services(self, request_mock):
        mock = mock_request(request_mock, 200, ['service'])
        services = self.client.list_services()
        mock.request.assert_called_with('GET', '/account/services')
        self.assertEqual(services, ['service'])

    @mock.patch("bss_client.client.Request")
    def test_list_services_with_category(self, request_mock):
        mock = mock_request(request_mock, 200, ['service'])
        services = self.client.list_services(category='mycategory')
        mock.add_param.assert_called_with('category', 'mycategory')
        mock.request.assert_called_with('GET', '/account/services')
        self.assertEqual(services, ['service'])

    @mock.patch("bss_client.client.Request")
    def test_list_catalog(self, request_mock):
        mock = mock_request(request_mock, 200, ['cat'])
        catalog = self.client.list_catalog()
        mock.add_param.assert_called_with('expand', 'productBundleRevisions')
        mock.request.assert_called_with('GET', '/account/catalog')
        self.assertEqual(catalog, ['cat'])

    @mock.patch("bss_client.client.Request")
    def test_list_catalog_with_expand(self, request_mock):
        mock = mock_request(request_mock, 200, ['cat'])
        catalog = self.client.list_catalog(expand='someOther')
        mock.add_param.assert_called_with('expand', 'someOther')
        mock.request.assert_called_with('GET', '/account/catalog')
        self.assertEqual(catalog, ['cat'])

    @mock.patch("bss_client.client.Request")
    def test_list_subscriptions(self, request_mock):
        mock = mock_request(request_mock, 200, ['sub'])
        result = self.client.list_subscriptions()
        mock.request.assert_called_with('GET', '/subscriptions')
        self.assertEqual(result, ['sub'])

    @mock.patch("bss_client.client.Request")
    def test_get_user(self, request_mock):
        mock = mock_request(request_mock, 200, ['user'])
        result = self.client.get_user('uuid')
        mock.request.assert_called_with('GET', '/users/uuid')
        self.assertEqual(result, ['user'])

    @mock.patch("bss_client.client.Request")
    def test_get_account(self, request_mock):
        mock = mock_request(request_mock, 200, ['account'])
        result = self.client.get_account()
        mock.request.assert_called_with('GET', '/account')
        self.assertEqual(result, ['account'])
