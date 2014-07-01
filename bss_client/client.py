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
        if 200 <= rsp.status_code < 300:
            return rsp.json()
        raise BSSError(rsp.status_code, rsp.text)

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

    def get_subscription(self, subscription_uuid, expand=None):
        req = self.create_request()
        if expand:
            req.add_param('expand', expand)
        rsp = req.request('GET', '/subscriptions/{0}'.format(subscription_uuid))
        return self._handle_json_response(rsp)

    def create_subscription(self, configurationdata, context, productbundleid,
                            resourcetype, serviceinstanceuuid, tenantparam=None):
        req = self.create_request()
        req.add_param('provision', 'true')
        req.add_param('configurationdata', configurationdata)
        req.add_param('context', context)
        req.add_param('productbundleid', productbundleid)
        req.add_param('resourcetype', resourcetype)
        req.add_param('serviceinstanceuuid', serviceinstanceuuid)
        if not tenantparam:
            tenantparam = self.get_account()['account']['uuid']
        req.add_param('tenantparam', tenantparam)
        rsp = req.request('POST', '/subscriptions')
        return self._handle_json_response(rsp)

    def delete_subscription(self, subscription_uuid):
        req = self.create_request()
        rsp = req.request('DELETE', '/subscriptions/{0}'.format(subscription_uuid))
        return self._handle_json_response(rsp)
