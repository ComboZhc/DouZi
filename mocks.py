#coding: utf-8
import json
from requests import codes
from client import s

def get(url, **kwargs):
    if url == "/users/1/":
        return codes.ok, s({
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
        return codes.ok, s(
            [{
                'topic_id':1,
                'user_id':1,
                'image_id':1,
                'title':u'吃西瓜',
                'content':u'吃吃拆此航次吃',
                'is_public':1,
            }, {
                'topic_id':2,
                'user_id':1,
                'image_id':2,
                'title':u'还有比奶子更丧的么',
                'content':u'RT',
                'is_public':1,
            }, {
                'topic_id':3,
                'user_id':1,
                'image_id':3,
                'title':u'sbPJ撸个蛋啊',
                'content':u'sb滚粗',
                'is_public':1,
            }, {
                'topic_id':4,
                'user_id':1,
                'image_id':4,
                'title':u'垃圾游戏，怒删',
                'content':u'天凤就是个垃圾游戏，不服来辩',
                'is_public':1,
            }])
    elif url == "/users/":
        return codes.ok, s(
            [{
                'username':'sb',
                'user_id':2,
                'email':'papapa@fudan.edu.cn',
                'gender':'m',
                'phone':'123431423',
                'location':'大张江',
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1
            },
            {
                'username':'马奶子',
                'user_id':3,
                'email':'sb@fudan.edu.cn',
                'gender':'f',
                'phone':'123431423',
                'location':'公共厕所',
                'is_vip':0,
                'is_banned':1,
                'is_admin':0,
                'is_public':1
            },
            {
                'username':'克长',
                'user_id':4,
                'email':'bbbb@fudan.edu.cn',
                'gender':'m',
                'phone':'123431423',
                'location':'美帝',
                'is_vip':1,
                'is_banned':0,
                'is_admin':0,
                'is_public':1
            },
            {
                'username':'陈叔叔',
                'user_id':5,
                'email':'doubi@fudan.edu.cn',
                'gender':'m',
                'phone':'123431423',
                'location':'dota',
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1
            }
            ])
    elif url == "/topics/1/" or url == "/topics/2/" or url == "/topics/3/" or url == "/topics/4/":
        return codes.ok, s({
                'topic_id':1,
                'user_id':1,
                'image_id':'1.jpg',
                'title':u'吃西瓜',
                'content':u'吃吃拆此航次吃',
                'is_public':1
        })
    return 0, None

def post(url, data={}, **kwargs):
    data = s(json.loads(data))
    if url == '/login/':
        if data['username'] == data['password']:
            return codes.ok, s({
                'user_id':1,
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1, 
            })
        else:
            return codes.unauthorized, s({})
    elif url == '/users/':
        return codes.created, s({'user_id':1})
    elif url == '/topics/':
        return codes.created, s({'topic_id':1})
    return 0, None

def put(url, data={}, **kwargs):
    if url == "/users/1/":
        return codes.accepted, s({})
    elif url == "/topics/1/" or url == "/topics/2/" or url == "/topics/3/" or url == "/topics/4/":
        return codes.ok, None
    return 0, None

    
def delete(url, data={}, **kwargs):
    if url == "/topics/1/" or url == "/topics/2/" or url == "/topics/3/" or url == "/topics/4/":
        return codes.ok, None
    return 0, None