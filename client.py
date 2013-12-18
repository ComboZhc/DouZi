import requests
import web
import json
from simplejson import JSONDecodeError
from utils import storify

import mocks

mock = True
base = 'http://lixiao.3owl.com/'

def get(url, **kwargs):
    if mock:
        r, j = mocks.get(url, **kwargs)
        print url, r, j
        return r, storify(j)
    else:
        r = requests.get(base + url, **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def options(url, **kwargs):
    if mock:
        r, j = mocks.options(url, **kwargs)
        return r, storify(j)
    else:
        r = requests.options(base + url, **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def head(url, **kwargs):
    if mock:
        r, j = mocks.head(url, **kwargs)
        return r, storify(j)
    else:
        r = requests.head(base + url, **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def post(url, data={}, **kwargs):
    if mock:
        r, j = mocks.post(url, data=data, **kwargs)
        return r, storify(j)
    else:
        r = requests.post(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def put(url, data={}, **kwargs):
    if mock:
        r, j = mocks.put(url, data=data, **kwargs)
        return r, storify(j)
    else:
        r = requests.put(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def patch(url, data={}, **kwargs):
    if mock:
        r, j = mocks.patch(url, data=data, **kwargs)
        return r, storify(j)
    else:
        r = requests.patch(base + url, data=json.dumps(data), **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})

def delete(url, **kwargs):
    if mock:
        r, j = mocks.delete(url, **kwargs)
        return r, storify(j)
    else:
        r = requests.delete(base + url, **kwargs)
        try:
            return r.status_code, storify(r.json())
        except JSONDecodeError:
            return r.status_code, storify({})
