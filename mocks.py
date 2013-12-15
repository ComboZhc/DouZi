#coding: utf-8
import json
from requests import codes
from client import s

users = [s({
    'username':'ComboZhc',
    'user_id':5,
    'email':'zhangchao6865@gmail.com',
    'gender':'m',
    'phone':'123456789',
    'description':u'人固有一死，或重于泰山，或轻于鸿毛',
    'location':u'上海',
    'is_vip':0,
    'is_banned':0,
    'is_admin':0,
    'is_public':1, 
}), s({
    'username':'Yuehan',
    'user_id':2,
    'email':'main.yuehanxu@gmail.com',
    'gender':'f',
    'phone':'123456789',
    'description':u'我是LOL狗',
    'location':u'上海',
    'is_vip':0,
    'is_banned':0,
    'is_admin':0,
    'is_public':0, 
}), s({
    'username':'Sangbi',
    'user_id':3,
    'email':'meishadia@gmail.com',
    'gender':'m',
    'phone':'18801734044',
    'phone':'123456789',
    'description':u'呵呵',
    'location':'床上',
    'is_vip':0,
    'is_banned':0,
    'is_admin':0,
    'is_public':0, 
})]

u = users[0]
u2 = users[1]
u3 = users[2]

def get(url, **kwargs):
    if url == "/users/1/":
        return codes.ok, u
    elif url == "/users/2/":
        return codes.ok, u2
    elif url == "/topics/" or url == "/users/1/topics/" or url == "/topics/hot/":
        return codes.ok, s(
            [{
                'topic_id':1,
                'creator':u,
                'image_id':1,
                'title':u'吃西瓜',
                'content':u'吃吃吃吃吃吃吃吃吃吃吃吃吃吃吃',
                'is_public':1,
            }, {
                'topic_id':2,
                'creator':u2,
                'image_id':2,
                'title':u'还有比奶子更丧的么',
                'content':u'RT',
                'is_public':1,
            }, {
                'topic_id':3,
                'creator':u2,
                'image_id':3,
                'title':u'这PJ撸个蛋啊',
                'content':u'sb滚粗',
                'is_public':1,
            }, {
                'topic_id':4,
                'creator':u3,
                'image_id':4,
                'title':u'垃圾游戏，怒删',
                'content':u'天凤就是个垃圾游戏，不服来辩',
                'is_public':1,
            }])
    elif url == "/users/" or url == "/bans/" or url == "/vips/" or url == "/vips/pending/":
        return codes.ok, s(
            [u,u2,u3,{
                "username":"Yuehan Xu",
                "user_id":"4",
                "email":"admin@localhost",
                "gender":"f",
                "phone":"1234567890",
                "location":"Tokyo",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"0"
            },{
                "username":"Li Xiao",
                "user_id":"5",
                "email":"xiaoli@localhost",
                "gender":"f",
                "phone":"12345",
                "location":"Universe",
                "is_vip":"1",
                "is_banned":"0",
                "is_admin":"1",
                "is_public":"1"
            },{"username":"Xiao Li",
                "user_id":"7",
                "email":"lixiao@localhost",
                "gender":"m",
                "phone":"12453",
                "location":"China",
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
                'content':u'吃吃吃吃吃吃吃吃吃吃吃吃吃吃吃',
                'is_public':1,
        })
    elif url == "/topics/1/comments/" or url == "/topics/2/comments/" or url == "/topics/3/comments/" or url == "/topics/4/comments/":
        return codes.ok, s([
                {
                    'comment_id':1,
                    'creator':u,
                    'content':'撸主挽尊',
                },
                {
                    'comment_id':2,
                    'creator':u,
                    'content':'楼上',
                }
            ])
    elif url == "/groups/" or url == "/users/1/groups/":
        return codes.ok, s([
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator': u
                },
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组2',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator': u2
                },
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组3',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator': u3
                }
            ])
    elif url == "/groups/1/":
        return codes.ok, s(
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator':u3,
                    'members':[u, u2,
                        {
                            'user_id':3,
                            'username':'陈乃',
                            'email':'cldtc@gmail.com',
                            'gender':'1',
                            'phone':'18801733333',
                            'location':'床上',
                            'is_vip':0,
                            'is_admin':0
                        },
                        {
                            'user_id':4,
                            'username':'sb',
                            'email':'meishadia@gmail.com',
                            'gender':'1',
                            'phone':'18801734044',
                            'location':'床上',
                            'is_vip':1,
                            'is_admin':0
                        }
                    ]
                })
    elif url == '/users/1/groups/requests/':
        return codes.ok, s([
            {
                'user_id':2,
                'group_name':'吃奶子俱乐部',
                'username':'manaizi',
                'group_id':1
            },
            {
                'user_id':3,
                'group_name':'吃奶子',
                'username':'nitianwosha',
                'group_id':2
            }])
    return 0, None

def post(url, data={}, **kwargs):
    data = s(json.loads(data))
    if url == '/login/':
        if data.username == data.password:
            return codes.ok, s({
                'user_id':1,
                'is_vip':1 if data.username == 'vip' else 0,
                'is_banned':1 if data.username == 'ban' else 0,
                'is_admin':1 if data.username == 'admin' else 0,
                'is_public':1, 
            })
        else:
            return codes.unauthorized, s({})
    elif url == '/users/':
        return codes.created, s({'user_id':1})
    elif url == '/topics/':
        return codes.created, s({'topic_id':1})
    elif url == '/topics/1/comments/':
        return codes.created, s({})
    elif url == '/users/1/friends/' or url == '/users/2/friends/':
        return codes.created, s({})
    elif url == '/notifications/new/':
        return codes.created, s({})
    elif url == '/groups/':
        return codes.created, s({'group_id':1})
    elif url == '/groups/1/requests/':
        return codes.created, s({})
    elif url == '/groups/1/requests/3/':
        return codes.created, s({})
    return 0, None

def put(url, data={}, **kwargs):
    if url == "/users/1/":
        return codes.accepted, s({})
    elif url == '/vips/1/0/' or url == '/vips/1/1/' or url == '/vips/1/2/':
        return codes.ok, s({})
    return 0, None

    
def delete(url, data={}, **kwargs):
    if url == "/topics/1/comments/1/" or url == "/topics/1/comments/2/":
        return codes.accepted, s({})
    elif url == "/groups/1/":
        return codes.accepted, s({})
    return 0, None