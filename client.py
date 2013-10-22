import requests
import web
import json
from simplejson import JSONDecodeError

def s(mapping):
    if isinstance(mapping, dict):
        return web.storify(mapping)
    if isinstance(mapping, list):
        return [web.storify(x) for x in mapping]
        
import mocks

mock = False
base = 'http://lixiao.3owl.com/'

def get(url, **kwargs):
    if mock:
        return mocks.get(url, **kwargs)
    else:
        r = requests.get(base + url, **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def options(url, **kwargs):
    if mock:
        return mocks.options(url, **kwargs)
    else:
        r = requests.options(base + url, **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def head(url, **kwargs):
    if mock:
        return mocks.head(url, **kwargs)
    else:
        r = requests.head(base + url, **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def post(url, data={}, **kwargs):
    if mock:
        return mocks.post(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.post(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def put(url, data={}, **kwargs):
    if mock:
        return mocks.put(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.put(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def patch(url, data={}, **kwargs):
    if mock:
        return mocks.patch(url, data=json.dumps(data), **kwargs)
    else:
        r = requests.patch(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})

def delete(url, **kwargs):
    if mock:
        return mocks.delete(url, **kwargs)
    else:
        r = requests.delete(base + url, **kwargs)
        try:
            return r.status_code, s(r.json())
        except JSONDecodeError:
            return r.status_code, s({})
