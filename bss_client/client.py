from bss_client.exception import BSSError
from bss_client.request import Request


class BSSClient(object):

    def __init__(self, endpoint, key, secret, requests_params=None):
        self.endpoint = endpoint
        self.key = key
        self.secret = secret
        if requests_params is None:
            self.requests_params = {}
        else:
            self.requests_params = requests_params

    def create_request(self):
        return Request(self.endpoint, self.key, self.secret,
                       **self.requests_params)

    def _handle_json_response(self, rsp):
        if rsp.status_code != 200:
            raise BSSError(rsp.status_code, rsp.text)
        return rsp.json()

    def list_services(self, category=None):
        req = self.create_request()
        if category:
            req.add_param('category', category)
        path = '/account/services'
        rsp = req.request('GET', path)
        return self._handle_json_response(rsp)

    def list_catalog(self, expand='productBundleRevisions'):
        req = self.create_request()
        req.add_param('expand', expand)
        rsp = req.request('GET', '/account/catalog')
        return self._handle_json_response(rsp)

    def list_subscriptions(self):
        req = self.create_request()
        req.add_param('expand', 1)
        rsp = req.request('GET', '/subscriptions')
        return self._handle_json_response(rsp)

    def get_user(self, user_id):
        req = self.create_request()
        rsp = req.request('GET', '/users/{0}'.format(user_id))
        return self._handle_json_response(rsp)

    def get_account(self):
        req = self.create_request()
        rsp = req.request('GET', '/account')
        return self._handle_json_response(rsp)
