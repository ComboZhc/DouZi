#coding: utf-8
import json
import re
from requests import codes
from utils import update_by_key, update_by_key_int, storify

users = [{
    'user_id':0,
    'username':'admin',
    'password':'admin',
    'email':'zhangchao6865@gmail.com',
    'gender':'m',
    'phone':'123456789',
    'description':u'人固有一死，或重于泰山，或轻于鸿毛',
    'location':u'上海',
    'is_vip':0,
    'is_banned':0,
    'is_admin':1,
    'is_public':1, 
}, {
    'user_id':1,
    'username':'vip',
    'password':'vip',
    'email':'main.yuehanxu@gmail.com',
    'gender':'f',
    'phone':'18801733864',
    'description':u'我喜欢LOL',
    'location':u'沧州',
    'is_vip':1,
    'is_banned':0,
    'is_admin':0,
    'is_public':1, 
}, {
    'user_id':2,
    'username':'ban',
    'password':'ban',
    'email':'cldtc@gmail.com',
    'gender':'m',
    'phone':'18801733923',
    'description':u'DOTA万岁',
    'location':u'丹阳',
    'is_vip':0,
    'is_banned':1,
    'is_admin':0,
    'is_public':1, 
}, {
    'user_id':3,
    'username':'private',
    'password':'private',
    'email':'meshiadia@gmail.com',
    'gender':'f',
    'phone':'18801734044',
    'description':u'天凤就是个垃圾游戏，不服来辩',
    'location':u'宁波',
    'is_vip':0,
    'is_banned':0,
    'is_admin':0,
    'is_public':0, 
}, {
    'user_id':4,
    'username':'user',
    'password':'user',
    'email':'user@gmail.com',
    'gender':'m',
    'phone':'18801733333',
    'description':u'BILIBILI',
    'location':u'北京',
    'is_vip':0,
    'is_banned':0,
    'is_admin':0,
    'is_public':1,
}]

friends = [
    [users[1]],
    [users[2], users[3]],
    [users[3]],
    [users[0]],
    [users[0]],
]

def get(url, **kwargs):
    if re.match(r'^/users/(?P<id>\d+)/$', url):
        i = int(re.match(r'^/users/(?P<id>\d+)/$', url).group('id'))
        if i < len(users):
            return codes.ok, users[i]
        else:
            return codes.bad, {}
    elif re.match(r'^/users/(?P<id>\d+)/friends/$', url):
        i = int(re.match(r'^/users/(?P<id>\d+)/friends/$', url).group('id'))
        if i < len(friends):
            return codes.ok, friends[i]
        else:
            return codes.bad, {}
    elif url == "/topics/" or url == "/users/1/topics/" or url == "/topics/hot/":
        return codes.ok, storify(
            [{
                'topic_id':1,
                'creator':users[0],
                'image_id':1,
                'title':u'吃西瓜',
                'content':u'吃吃吃吃吃吃吃吃吃吃吃吃吃吃吃',
                'is_public':1,
            }, {
                'topic_id':2,
                'creator':users[1],
                'image_id':2,
                'title':u'还有比奶子更丧的么',
                'content':u'RT',
                'is_public':1,
            }, {
                'topic_id':3,
                'creator':users[1],
                'image_id':3,
                'title':u'这PJ撸个蛋啊',
                'content':u'sb滚粗',
                'is_public':1,
            }, {
                'topic_id':4,
                'creator':users[2],
                'image_id':4,
                'title':u'垃圾游戏，怒删',
                'content':u'天凤就是个垃圾游戏，不服来辩',
                'is_public':1,
            }])
    elif url == "/users/":
        return codes.ok, users
    elif url == "/bans/" or url == "/vips/" or url == "/vips/pending/":
        return codes.ok, storify(
            [u,users[1],users[2],{
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
        return codes.ok, storify({
                'topic_id':1,
                'creator':u,
                'image_id':'1.jpg',
                'title':u'吃西瓜',
                'content':u'吃吃吃吃吃吃吃吃吃吃吃吃吃吃吃',
                'is_public':1,
        })
    elif url == "/topics/1/comments/" or url == "/topics/2/comments/" or url == "/topics/3/comments/" or url == "/topics/4/comments/":
        return codes.ok, storify([
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
        return codes.ok, storify([
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator': u
                },
                {
                    'group_id':2,
                    'name':u'读书小组',
                    'brief':u'书是人类进步的阶梯',
                    'creator': users[1]
                },
                {
                    'group_id':3,
                    'name':u'LOL小组',
                    'brief':u'一起来玩吧',
                    'creator': users[2]
                }
            ])
    elif url == "/groups/1/":
        return codes.ok, storify(
                {
                    'group_id':1,
                    'name':u'吃奶子兴趣小组',
                    'brief':u'陈年马奶子，欢迎来吃',
                    'creator':u,
                    'members':[u, users[1], users[2],
                        {
                            'user_id':3,
                            'username':'陈叔叔',
                            'email':'cldtc@gmail.com',
                            'gender':'1',
                            'phone':'18801733333',
                            'location':'床上',
                            'is_vip':0,
                            'is_admin':0
                        },
                        {
                            'user_id':4,
                            'username':'逗比',
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
        return codes.ok, storify([
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
    elif url == '/notifications/':
        return codes.ok, storify([
                {
                    'notification_id':1,
                    'title':'看看这个话题',
                    'content':'马奶子最喜欢吃什么啊？<a href="/topics/1/">#马奶子吃吃吃#</a>',
                    'creator': users[0]
                },
                {
                    'notification_id':1,
                    'title':'来加入马奶子小组吧',
                    'content':'欢迎加入',
                    'creator': users[0]
                },
                {
                    'notification_id':1,
                    'title':'来加入马奶子小组吧',
                    'content':'欢迎加入',
                    'creator': 
                    {
                        'user_id':1,
                        'username':'奶子',
                        'email':'meishadia@gmail.com',
                        'gender':'m',
                        'phone':'1234567',
                        'location':'shanghai',
                        'is_vip':1
                    }
                }
            ])
    return 0, None

def post(url, data={}, **kwargs):
    if url == '/login/':
        for u in users:
            if u['username'] == data['username'] and u['password'] == data['password']:
                return codes.ok, u
        return codes.unauthorized, {}
    elif url == '/users/':
        for u in users:
            if u['username'] == data['username']:
                return codes.bad, {}
        users.append({})
        friends.append([])
        users[-1]['user_id'] = len(users) - 1
        users[-1]['username'] = data['username']
        users[-1]['password'] = data['password']
        users[-1]['email'] = data['email']
        users[-1]['gender'] = data['gender']
        users[-1]['phone'] = data['phone']
        users[-1]['location'] = data['location']
        users[-1]['description'] = data['description']
        users[-1]['is_admin'] = int(data['is_admin'])
        users[-1]['is_vip'] = 0
        users[-1]['is_banned'] = 0
        users[-1]['is_public'] = int(data['is_public'])
        return codes.created, len(users) - 1
    elif url == '/topics/':
        return codes.created, storify({'topic_id':1})
    elif url == '/topics/1/comments/':
        return codes.created, storify({})
    elif url == '/users/1/friends/' or url == '/users/2/friends/':
        return codes.created, storify({})
    elif url == '/notifications/new/':
        return codes.created, storify({})
    elif url == '/groups/':
        return codes.created, storify({'group_id':1})
    elif url == '/groups/1/requests/':
        return codes.created, storify({})
    return 0, None

def put(url, data={}, **kwargs):
    if re.match(r"^/users/(?P<id>\d+)/$", url):
        i = int(re.match(r"^/users/(?P<id>\d+)/$", url).group('id'))
        if i < len(users):
            update_by_key(users[i], data, 'username')
            update_by_key(users[i], data, 'password')
            update_by_key(users[i], data, 'email')
            update_by_key(users[i], data, 'gender')
            update_by_key(users[i], data, 'phone')
            update_by_key(users[i], data, 'location')
            update_by_key(users[i], data, 'description')
            update_by_key_int(users[i], data, 'is_admin')
            update_by_key_int(users[i], data, 'is_vip')
            update_by_key_int(users[i], data, 'is_banned')
            update_by_key_int(users[i], data, 'is_public')
            return codes.accepted, {}
        else:
            return codes.bad, {}
    elif url == '/vips/1/0/' or url == '/vips/1/1/' or url == '/vips/1/2/':
        return codes.ok, storify({})
    return 0, None

    
def delete(url, data={}, **kwargs):
    if url == "/topics/1/comments/1/" or url == "/topics/1/comments/2/":
        return codes.accepted, storify({})
    elif url == "/groups/1/":
        return codes.accepted, storify({})
    return 0, None