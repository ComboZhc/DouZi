#coding: utf-8
import json
from requests import codes
from client import s

u = s({
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

def get(url, **kwargs):
    if url == "/users/1/":
        return codes.ok, u
    elif url == "/topics/" or url == "/users/1/topics/":
        return codes.ok, s(
            [{
                'topic_id':1,
                'creator':u,
                'image_id':1,
                'title':u'吃西瓜',
                'content':u'吃吃拆此航次吃',
                'is_public':1,
            }, {
                'topic_id':2,
                'creator':u,
                'image_id':2,
                'title':u'还有比奶子更丧的么',
                'content':u'RT',
                'is_public':1,
            }, {
                'topic_id':3,
                'creator':u,
                'image_id':3,
                'title':u'sbPJ撸个蛋啊',
                'content':u'sb滚粗',
                'is_public':1,
            }, {
                'topic_id':4,
                'creator':u,
                'image_id':4,
                'title':u'垃圾游戏，怒删',
                'content':u'天凤就是个垃圾游戏，不服来辩',
                'is_public':1,
            }])
    elif url == "/users/" or url == "/bans/" or url == "/vips/" or url == "/vips/pending/":
        return codes.ok, s(
            [{
                "username":"admin",
                "user_id":"1",
                "email":"admin@localhost",
                "gender":"m",
                "phone":"1234567890",
                "location":"localhost",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"0"
            },{
                "username":"aaa",
                "user_id":"1",
                "email":"admin@localhost",
                "gender":"m",
                "phone":"1234567890",
                "location":"localhost",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"0"
            },{
                "username":"bbb",
                "user_id":"1",
                "email":"admin@localhost",
                "gender":"m",
                "phone":"1234567890",
                "location":"localhost",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"0"
            },{
                "username":"ccc",
                "user_id":"1",
                "email":"admin@localhost",
                "gender":"m",
                "phone":"1234567890",
                "location":"localhost",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"0"
            },{
                "username":"xiaoli",
                "user_id":"5",
                "email":"xiaoli@localhost",
                "gender":"m",
                "phone":"12345",
                "location":"bfgd",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"1"
            },{"username":"lixiao",
                "user_id":"7",
                "email":"lixiao@localhost",
                "gender":"m",
                "phone":"12453",
                "location":"localhost",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"1"
            }])
    elif url == "/topics/1/" or url == "/topics/2/" or url == "/topics/3/" or url == "/topics/4/":
        return codes.ok, s({
                'topic_id':1,
                'creator':u,
                'image_id':'1.jpg',
                'title':u'吃西瓜',
                'content':u'吃吃拆此航次吃',
                'is_public':1,
        })
    elif url == "/topics/1/comments/":
        return codes.ok, s([
                {
                    'creator':u,
                    'content':'lzsb',
                },
                {
                    'creator':u,
                    'content':'lzsb',
                }
            ])
    return 0, None

def post(url, data={}, **kwargs):
    data = s(json.loads(data))
    if url == '/login/':
        if data['username'] == data['password']:
            return codes.ok, s({
                'user_id':1,
                'is_vip':0,
                'is_banned':0,
                'is_admin':1,
                'is_public':1, 
            })
        else:
            return codes.unauthorized, s({})
    elif url == '/users/':
        return codes.created, s({'user_id':1})
    elif url == '/topics/':
        return codes.created, s({'topic_id':1})
    elif url == '/topics/1/comments/':
        return codes.ok, s({})
    elif url == '/vips/1/':
        return codes.ok, s({})
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