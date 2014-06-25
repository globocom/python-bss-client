from collections import OrderedDict
import urllib
import hashlib
import hmac
import base64
import time

import requests


class Request(object):

    def __init__(self, endpoint, key, secret, **kwargs):
        self.endpoint = endpoint
        self.key = key
        self.secret = secret
        self.requests_params = {
            'headers': {'Content-Type': 'application/json'}
        }
        self.requests_params.update(kwargs)
        self.params = {
            'apiKey': self.key
        }

    def add_param(self, key, value):
        current_value = self.params.get(key, [])
        if isinstance(value, list):
            current_value = current_value + value
        else:
            current_value.append(value)
        self.params[key] = current_value

    def _sign(self, path):
        self.params['_'] = int(time.time() * 1000)
        ordered_params = OrderedDict()
        for key, value in sorted(self.params.items()):
            ordered_params[key] = value
        params_str = urllib.urlencode(ordered_params, doseq=True)
        path = "/{0}".format(path.lstrip('/'))
        signature_str = path + params_str.lower()
        hmac_dig = hmac.new(self.secret, signature_str, hashlib.sha1).digest()
        signature = urllib.quote(base64.encodestring(hmac_dig).strip())
        params_str = "{0}&signature={1}".format(params_str, signature)
        url = "{0}{1}?{2}".format(self.endpoint.rstrip('/'), path, params_str)
        return url

    def request(self, method, path):
        url = self._sign(path)
        rsp = requests.request(method.upper(), url,
                               **self.requests_params)
        return rsp
