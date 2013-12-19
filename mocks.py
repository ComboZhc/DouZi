#coding: utf-8
import json
import re
import _
from requests import codes
from utils import storify

class NotFoundException(Exception):
    pass

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
    'friends': [1],
    'notifications': [],
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
    'friends': [0],
    'notifications': [],
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
    'friends': [2, 3],
    'notifications': [],
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
    'friends': [3],
    'notifications': [],
}, None,
{
    'user_id':5,
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
    'friends': [0],
    'notifications': [],
}]

topics = [{
    'topic_id':0,
    'image_id':'1.jpg',
    'title':u'一个公开的话题',
    'content':u'这是一个公开的话题',
    'is_public':1,
    'creator_id':0,
    'user_id':0,
    'comments':[],
},{
    'topic_id':1,
    'image_id':'2.jpg',
    'title':u'一个私密的话题',
    'content':u'这是一个私密的话题',
    'is_public':0,
    'creator_id':5,
    'user_id':5,
    'comments':[],
},None,{
    'topic_id':3,
    'image_id':'4.jpg',
    'title':u'一个新的话题',
    'content':u'这是一个新的话题',
    'is_public':1,
    'creator_id':5,
    'user_id':5,
    'comments':[],
}]

groups = [{
    'group_id':0,
    'name':u'管理员小组',
    'brief':u'只有管理员在的组',
    'creator_id':0,
    'members':[],
    'requests':[],
},None,{
    'group_id':2,
    'name':u'大家的小组',
    'brief':u'好多人在这个小组',
    'creator_id':0,
    'members':[users[1],users[2],users[3]],
    'requests':[],
}]

def get_user_by_id(id):
    for u in users:
        if u and u['user_id'] == int(id):
            return u
    raise NotFoundException()

def get_users_by_ids(ids):
    return [get_user_by_id(id) for id in ids]

def get_friends_by_id(id):
    user = get_user_by_id(id)
    return get_users_by_ids(user['friends'])

def get_topic_by_id(id):
    for t in topics:
        if t and t['topic_id'] == int(id):
            return t
    raise NotFoundException()

def get_group_by_id(id):
    for g in groups:
        if g and g['group_id'] == int(id):
            return g
    raise NotFoundException()

def update_by_key_int(a, b, key):
    if key in b:
        a[key] = int(b[key])

def update_by_key(a, b, key):
    if key in b:
        a[key] = b[key]

def get(url, **kwargs):
    try:
        if url == "/users/":
            return codes.ok, filter(lambda u:u, users)
        if re.match(r'^/users/(?P<id>\d+)/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/$', url).group('id'))
            return codes.ok, get_user_by_id(id)
        if re.match(r'^/users/(?P<id>\d+)/friends/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/friends/$', url).group('id'))
            return codes.ok, get_friends_by_id(id)
        if re.match(r'^/users/(?P<id>\d+)/topics/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/topics/$', url).group('id'))
            return codes.ok, filter(lambda t:t and t['creator_id'] == id, topics)
        if re.match(r'^/users/(?P<id>\d+)/notifications/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/notifications/$', url).group('id'))
            user = get_user_by_id(id)
            return codes.ok, user['notifications']
        if re.match(r'^/users/(?P<id>\d+)/groups/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/groups/$', url).group('id'))
            user = get_user_by_id(id)
            return codes.ok, filter(lambda g:g and (g['creator_id'] == id or user in g['members']), groups)
        if re.match(r'^/users/(?P<id>\d+)/groups/requests/$', url):
            id = int(re.match(r'^/users/(?P<id>\d+)/groups/requests/$', url).group('id'))
            user = get_user_by_id(id)
            gs = filter(lambda g:g and (g['creator_id'] == id or user in g['members']), groups)
            result = []
            for g in gs:
                for r in g['requests']:
                    result.append({})
                    result[-1]['group_name'] = g['name']
                    result[-1]['group_id'] = g['group_id']
                    result[-1]['username'] = r['username']
                    result[-1]['user_id'] = r['user_id']
            return codes.ok, result
        if url == "/bans/":
            return codes.ok, filter(lambda u:u and u['is_banned'] == 1, users)
        if url == "/vips/":
            return codes.ok, filter(lambda u:u and u['is_vip'] == 1, users)
        if url == "/vips/pending/":
            return codes.ok, filter(lambda u:u and u['is_vip'] == 2, users)
        if url == "/topics/":
            return codes.ok, filter(lambda t:t, topics)
        if url == "/topics/hot/":
            hot_topics = filter(lambda t:t, topics)
            hot_topics.sort(lambda a, b: - len(a['comments']) + len(b['comments']))
            return codes.ok, hot_topics
        if re.match(r'^/topics/(?P<id>\d+)/$', url):
            id = int(re.match(r'^/topics/(?P<id>\d+)/$', url).group('id'))
            return codes.ok, get_topic_by_id(id)
        if re.match(r'^/topics/(?P<id>\d+)/comments/$', url):
            id = int(re.match(r'^/topics/(?P<id>\d+)/comments/$', url).group('id'))
            return codes.ok, filter(lambda c:c, get_topic_by_id(id)['comments'])
        if url == "/groups/":
            return codes.ok, filter(lambda g:g, groups)
        if re.match(r'^/groups/(?P<id>\d+)/$', url):
            id = int(re.match(r'^/groups/(?P<id>\d+)/$', url).group('id'))
            return codes.ok, get_group_by_id(id)
    except NotFoundException:
        return codes.bad, {}
    return 0, None

def post(url, data={}, **kwargs):
    try:
        if url == '/login/':
            for u in users:
                if u and u['username'] == data['username'] and u['password'] == data['password']:
                    return codes.ok, u
            return codes.unauthorized, {}
        if url == '/users/':
            for u in users:
                if u and u['username'] == data['username']:
                    return codes.bad, {}
            users.append({})
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
            users[-1]['friends'] = []
            users[-1]['notifications'] = []
            return codes.created, users[-1]
        if url == '/topics/':
            topics.append({})
            topics[-1]['topic_id'] = len(topics) - 1
            topics[-1]['creator_id'] = int(data['user_id'])
            topics[-1]['user_id'] = int(data['user_id'])
            topics[-1]['image_id'] = data['image_id']
            topics[-1]['title'] = data['title']
            topics[-1]['content'] = data['content']
            topics[-1]['is_public'] = int(data['is_public'])
            topics[-1]['comments'] = []
            for user in users:
                if user and int(data['user_id']) in user['friends']:
                    user['notifications'].append({})
                    user['notifications'][-1]['user_id'] = int(data['user_id'])
                    user['notifications'][-1]['creator_id'] = int(data['user_id'])
                    user['notifications'][-1]['title'] = _.prefix.push
                    user['notifications'][-1]['content'] = '<a href="/topics/%i/">#%s#</a>' % (topics[-1]['topic_id'], data['title'])
            return codes.created, topics[-1]
        if re.match(r"^/users/(?P<id>\d+)/friends/$", url):
            id = int(re.match(r"^/users/(?P<id>\d+)/friends/$", url).group('id'))
            fid = int(data['friend_id'])
            user = get_user_by_id(id)
            for f in user['friends']:
                if f == fid:
                    return codes.bad, {}
            user['friends'].append(fid)
            return codes.created, {}
        if re.match(r'^/topics/(?P<id>\d+)/comments/$', url):
            id = int(re.match(r'^/topics/(?P<id>\d+)/comments/$', url).group('id'))
            topic = get_topic_by_id(id)
            user = get_user_by_id(int(data['creator_id']))
            topic['comments'].append({})
            topic['comments'][-1]['comment_id'] = len(topic['comments']) -1
            topic['comments'][-1]['content'] = data['content']
            topic['comments'][-1]['creator_id'] = user['user_id']
            topic['comments'][-1]['user_id'] = user['user_id']
            return codes.created, topic['comments'][-1]
        if url == '/notifications/new/':
            if data.get('receiver_id'):
                user = get_user_by_id(int(data['receiver_id']))
                user['notifications'].append({})
                user['notifications'][-1]['user_id'] = int(data['user_id'])
                user['notifications'][-1]['creator_id'] = int(data['user_id'])
                user['notifications'][-1]['title'] = data['title']
                user['notifications'][-1]['content'] = data['content']
            else:
                for user in users:
                    if user:
                        user['notifications'].append({})
                        user['notifications'][-1]['user_id'] = int(data['user_id'])
                        user['notifications'][-1]['creator_id'] = int(data['user_id'])
                        user['notifications'][-1]['title'] = data['title']
                        user['notifications'][-1]['content'] = data['content']
            return codes.created, {}
        if url == '/groups/':
            groups.append({})
            groups[-1]['group_id'] = len(groups) - 1
            groups[-1]['creator_id'] = int(data['user_id'])
            groups[-1]['user_id'] = int(data['user_id'])
            groups[-1]['name'] = data['name']
            groups[-1]['brief'] = data['brief']
            groups[-1]['members'] = []
            groups[-1]['requests'] = []
            return codes.created, groups[-1]
        if re.match(r'^/groups/(?P<id>\d+)/requests/$', url):
            id = int(re.match(r'^/groups/(?P<id>\d+)/requests/$', url).group('id'))
            group = get_group_by_id(id)
            user = get_user_by_id(int(data['user_id']))
            if user not in group['requests'] and user not in group['members']:
                group['requests'].append(user)
                return codes.created, {}
            return codes.bad, {}
        if re.match(r'^/groups/(?P<id>\d+)/requests/(?P<uid>\d+)/$', url):
            r = re.match(r'^/groups/(?P<id>\d+)/requests/(?P<uid>\d+)/$', url)
            id = int(r.group('id'))
            uid = int(r.group('uid'))
            group = get_group_by_id(id)
            user = get_user_by_id(uid)
            if user in group['requests']:
                group['members'].append(user)
                group['requests'].remove(user)
                return codes.created, {}
            return codes.bad, {}
    except NotFoundException:
        return codes.bad, {}
    return 0, None

def put(url, data={}, **kwargs):
    try:
        if re.match(r"^/users/(?P<id>\d+)/$", url):
            id = int(re.match(r"^/users/(?P<id>\d+)/$", url).group('id'))
            user = get_user_by_id(id)
            update_by_key(user, data, 'username')
            update_by_key(user, data, 'password')
            update_by_key(user, data, 'email')
            update_by_key(user, data, 'gender')
            update_by_key(user, data, 'phone')
            update_by_key(user, data, 'location')
            update_by_key(user, data, 'description')
            update_by_key_int(user, data, 'is_admin')
            update_by_key_int(user, data, 'is_vip')
            update_by_key_int(user, data, 'is_banned')
            update_by_key_int(user, data, 'is_public')
            return codes.accepted, {}
        if re.match(r'^/topics/(?P<id>\d+)/$', url):
            id = int(re.match(r'^/topics/(?P<id>\d+)/$', url).group('id'))
            topic = get_topic_by_id(id)
            update_by_key(topic, data, 'title')
            update_by_key(topic, data, 'content')
            update_by_key(topic, data, 'image_id')
            update_by_key(topic, data, 'is_public')
            return codes.accepted, {}
    except NotFoundException:
        return codes.bad, {}
    return 0, None

    
def delete(url, data={}, **kwargs):
    try:
        if re.match(r"^/users/(?P<id>\d+)/friends/(?P<fid>\d+)/$", url):
            r = re.match(r"^/users/(?P<id>\d+)/friends/(?P<fid>\d+)/$", url)
            id = int(r.group('id'))
            fid = int(r.group('fid'))
            user = get_user_by_id(id)
            for j in range(len(user['friends'])):
                if user['friends'][j] == fid:
                    del user['friends'][j]
                    return codes.accepted, {}
            return codes.bad, {}
        if re.match(r'^/topics/(?P<id>\d+)/$', url):
            id = int(re.match(r'^/topics/(?P<id>\d+)/$', url).group('id'))
            for j in range(len(topics)):
                if topics[j] and topics[j]['topic_id'] == id:
                    topics[j] = None
                    return codes.accepted, {}
            return codes.bad, {}
        if re.match(r"^/topics/(?P<id>\d+)/comments/(?P<cid>\d+)/$", url):
            r = re.match(r"^/topics/(?P<id>\d+)/comments/(?P<cid>\d+)/$", url)
            id = int(r.group('id'))
            cid = int(r.group('cid'))
            topic = get_topic_by_id(id)
            for j in range(len(topic['comments'])):
                if topic['comments'][j] and topic['comments'][j]['comment_id'] == cid:
                    topic['comments'][j] = None
                    return codes.accepted, {}
            return codes.bad, {}
        if re.match(r"^/groups/(?P<id>\d+)/$", url):
            id = int(re.match(r"^/groups/(?P<id>\d+)/$", url).group('id'))
            # Owner
            for j in range(len(groups)):
                if groups[j] and groups[j]['creator_id'] == int(data['user_id']):
                    groups[j] = None
                    return codes.accepted, {}
            # Members
            group = get_group_by_id(id)
            for j in range(len(group['members'])):
                if group['members'][j] and group['members'][j]['user_id'] == int(data['user_id']):
                    del group['members'][j]
                    return codes.accepted, {}
            return codes.bad, {}
        if re.match(r'^/groups/(?P<id>\d+)/requests/(?P<uid>\d+)/$', url):
            r = re.match(r'^/groups/(?P<id>\d+)/requests/(?P<uid>\d+)/$', url)
            id = int(r.group('id'))
            uid = int(r.group('uid'))
            group = get_group_by_id(id)
            user = get_user_by_id(uid)
            if user in group['requests']:
                group['requests'].remove(user)
                return codes.created, {}
            return codes.bad, {}
    except NotFoundException:
        return codes.bad, {}
    return 0, None