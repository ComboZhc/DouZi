#coding: utf-8
from web import storify

def get(url, **kwargs):
    return 0, None

def post(url, **kwargs):
    if url == "/login/":
        if kwargs['data']['username'] == kwargs['data']['password']:
            return 200, storify({
                'userid':1,
                'is_vip':0,
                'is_banned':0,
                'is_admin':0,
                'is_public':1, 
            })
        else:
            return 401, storify({})

    if url == "/user/1/":
        return 200, storify({
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

