#coding: utf-8
class login:
    fail = u'用户名或密码错误'
    ok = u'登陆成功'

class reg:
    fail = u'注册信息错误'
    ok = u'注册成功'
    password_mismatch = u'密码不一致'

class user:
    class edit:
        ok = u'修改成功'
        fail = u'修改信息错误'
    class friend:
        ok = u'关注好友成功'
        fail = u'已经关注了'
    class ban:
        ok = u'用户封禁/解封成功'
        fail = u'用户封禁/解封失败'

class topic:
    class new:
        ok = u'发布话题成功'
        fail = u'发布话题失败'
    class edit:
        ok = u'修改话题成功'
        fail = u'修改话题失败'

class vip:
    class set:
        ok = u'VIP修改成功'
        fail = u'VIP修改失败'
        class up:
            ok = u'VIP申请成功'

class notification:
    class new:
        ok = u'发送通知成功'
        fail = u'发送通知失败'
    class recommend:
        ok = u'推荐话题成功'
        fail = u'推荐话题失败'
    class ad:
        ok = u'发送广告成功'
        fail = u'发送广告失败'

class group:
    class new:
        ok = u'创建小组成功'
        fail = u'创建小组失败'

class prefix:
    ad = u'[广告]'
    recommend = u'[推荐话题]'