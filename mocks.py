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
    elif url == "/topics/":
        return (codes.ok, [
            storify({
            'topic_id':1,
            'user_id':1,
            'image_id':1,
            'title':'吃西瓜',
            'content':'吃吃拆此航次吃',
            'is_public':1
            }),
            storify({
            'topic_id':2,
            'user_id':1,
            'image_id':2,
            'title':'还有比奶子更丧的么',
            'content':'RT',
            'is_public':1
            }),
            storify({
            'topic_id':3,
            'user_id':1,
            'image_id':3,
            'title':'sbPJ撸个蛋啊',
            'content':'sb滚粗',
            'is_public':1
            }),
            storify({
            'topic_id':4,
            'user_id':1,
            'image_id':4,
            'title':'垃圾游戏，怒删',
            'content':'天凤就是个垃圾游戏，不服来辩',
            'is_public':1
            })])
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
