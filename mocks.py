#coding: utf-8
from web import storify
import json
from requests import codes

def get(url, **kwargs):
    if url == "/users/1/":
        return codes.ok, storify({
                'username':'ComboZhc',
                'user_id':1,
                'email':'zhangchao6865@gmail.com',
                'gender':'m',
                'phone':'123456789',
                'description':u'人固有一死，或重于泰山，或轻于鸿毛',
                'location':u'上海',
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1, 
            })
    return 0, None

def post(url, data={}, **kwargs):
    data = storify(json.loads(data))
    if url == '/login/':
        if data['username'] == data['password']:
            return codes.ok, storify({
                'user_id':1,
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1, 
            })
        else:
            return codes.unauthorized, storify({})
    if url == '/users/':
        return codes.created, storify({
                'user_id':1,
            })

    return 0, None

def put(url, data={}, **kwargs):
    if url == "/users/1/":
        return codes.accepted, storify({})

    return 0, None
