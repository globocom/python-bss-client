import unittest
import mock
from freezegun import freeze_time

from bss_client.request import Request


class TestRequest(unittest.TestCase):
    def test_request(self):
        req = Request("http://localhost", "xxx", "yyy")
        self.assertEqual(req.endpoint, "http://localhost")
        self.assertEqual(req.key, "xxx")
        self.assertEqual(req.secret, "yyy")
        self.assertEqual(req.params, {"apiKey": "xxx"})
        self.assertDictEqual(req.requests_params, {
            'headers': {'Content-Type': 'application/json'}
        })

    def test_request_with_kwargs(self):
        req = Request("http://localhost", "xxx", "yyy", x=1, y=2)
        self.assertDictEqual(req.requests_params, {
            'headers': {'Content-Type': 'application/json'},
            "x": 1,
            "y": 2,
        })

    def test_request_add_param(self):
        req = Request("http://localhost", "xxx", "yyy")
        req.add_param("foo", "bar")
        req.add_param("foo2", "bar2")
        req.add_param("foo", "xyz")
        self.assertDictEqual(req.params, {
            "apiKey": "xxx",
            "foo": ["bar", "xyz"],
            "foo2": ["bar2"]
        })

    @freeze_time("2014-07-10")
    @mock.patch("requests.request")
    def test_run(self, request_mock):
        response = mock.Mock()
        request_mock.return_value = response
        req = Request("http://localhost", "xxx", "yyy")
        req.add_param("xyz", "a")
        req.add_param("abc", "z")
        result = req.request("get", "something")
        self.assertEqual(result, response)
        qs = "?_=1404950400000&abc=z&apiKey=xxx&xyz=a" \
             "&signature=MYW/iD3G%2Be55pwt55xqbIl4ARSw%3D"
        request_mock.assert_called_with(
            "GET",
            "http://localhost/something" + qs,
            headers={"Content-Type": "application/json"})

    @freeze_time("2014-07-10")
    @mock.patch("requests.request")
    def test_run_kwargs(self, request_mock):
        response = mock.Mock()
        request_mock.return_value = response
        req = Request("http://localhost", "xxx", "yyy", verify=False)
        result = req.request("post", "/something")
        self.assertEqual(result, response)
        qs = "?_=1404950400000&apiKey=xxx" \
             "&signature=RXs3sh2ad85frf%2BGWVLLQ9f4dqs%3D"
        request_mock.assert_called_with(
            "POST",
            "http://localhost/something" + qs,
            headers={"Content-Type": "application/json"},
            verify=False)
