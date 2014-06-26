# CPBM BSS API Client

­CloudPortal™ Business Manager (CPBM) Business Support System (BSS) API Client

## Description

This is a minimal wrapper around CPBM BSS API.

It simplifies creating signed requests to the API and also implements a 
high-level abstraction for commonly used methods.

Ideally we'll implement high-level wrappers for every possible API calls,
however we're not there yet.

## Instalation

```
$ pip install bss-client
```

## Basic Usage

With high-level API wrapper

```python
from bss_client import BSSClient

endpoint = 'http://myhost.com/portal/api'
key = 'my api key'
secret = 'my api secret'

client = BSSClient(endpoint, key, secret)
rsp_json = client.list_subscriptions()
print rsp_json
```

With low-level signed request wrapper

```python
from bss_client import BSSClient

client = BSSClient(endpoint, key, secret)
req = client.create_request()
req.add_param('tenantparam', 'uuid')
req.add_param('productbundleid', 'mybundleid')
...
rsp = req.request('POST', '/subscriptions')
print rsp
```
