import web
import client
from requests import codes
import _
import os

urls = (
    r'/?', 'Home',
    r'/login/?', 'Login',
    r'/logout/?', 'Logout',
    r'/reg/?', 'Reg',
    r'/users/?','UserList',
    r'/users/(\d+)/ban/(\d+)/?','UserBan',
    r'/users/(\d+)/?', 'User',
    r'/users/(\d+)/edit/?', 'UserEdit',
    r'/users/(\d+)/friend/?', 'UserFriend',
    r'/topics/?','TopicList',
    r'/topics/hot/?','TopicHotList',
    r'/topics/new/?', 'TopicNew',
    r'/topics/my/?','TopicMy',
    r'/topics/(\d+)/','Topic',
    r'/topics/(\d+)/edit/?', 'TopicEdit',
    r'/topics/(\d+)/delete/?', 'TopicDelete',
    r'/topics/(\d+)/comments/?', 'TopicComment',
    r'/topics/(\d+)/comments/(\d+)/delete/?', 'TopicCommentDelete',
    r'/bans/?', 'BanList',
    r'/vips/?', 'VipList',
    r'/vips/pending/?', 'VipPending',
    r'/vips/(\d+)/(\d+)/?','VipSet',
    r'/bans/?', 'BanList',
    r'/notifications/new/?', 'NotificationsNew',
    r'/notifications/?', 'Notifications',
    r'/groups/new/?', 'GroupNew',
    r'/groups/list/?', 'GroupList',
    r'/groups/my/?', 'GroupMy',
    r'/groups/(\d+)/?', 'Group',
    r'/groups/(\d+)/quit/?', 'GroupQuit',
    r'/groups/(\d+)/delete/?', 'GroupQuit',
    r'/groups/(\d+)/join/?', 'GroupJoin',
    r'/groups/(\d+)/approve/(\d+)/(\d+)/?', 'GroupApprove',
    r'/groups/requests/?', 'GroupRequests',
)
app = web.application(urls, globals())

#web.config.debug = True

session = None
if web.config.get('_session') is None:
    session = web.session.Session(app, 
        web.session.DiskStore('.sessions'), 
        initializer = {
             'user': {},
             'username': '',
             'message': '',
        }
    )
    web.config._session = session
else:
    session = web.config._session

def flash(message=None):
    if type(message) == str or type(message) == unicode:
        session.message = message
    elif type(message) == bool:
        message = session.message
        if message:
            session.message = None
        return message
    else:
        return session.message

def image_path(filename):
    return os.path.join('static', 'image', filename)

def image_gender(gender):
    if gender == 'm':
        return '<img width="16" height="16" src="/static/img/male.png"/>'
    else:
        return '<img width="16" height="16" src="/static/img/female.png"/>'

def user():
    return session.user

def is_admin():
    return session.user and session.user.is_admin == 1

def is_ingroup(group):
    for item in group.members:
        if item.user_id == session.user.user_id:
            return True
    return False

def is_vip():
    return session.user and session.user.is_vip == 1

def is_pending():
    return session.user and session.user.is_vip == 2

def is_banned():
    return session.user and session.user.is_banned == 1

class Home:
    def GET(self):
        if session.user:
            raise web.redirect('/topics/')
        else:
            render = web.template.render('asset', base='after.common', globals=globals())
            return render.topics_list(topics=[])

class Login:        
    def GET(self):
        render = web.template.render('asset', base='before.common', globals=globals())
        return render.login()

    def POST(self):
        i = web.input()
        r, j = client.post('/login/', data=i)
        if r == codes.ok:
            flash(_.login.ok)
            session.user = j
            session.username = i.username
            raise web.redirect("/")
        else:
            flash(_.login.fail)
            raise web.redirect('/login/')

class Logout:
    def GET(self):
        session.user = {}
        session.username = ''
        session.message = ''
        session.kill()
        raise web.redirect("/")

class Reg:
    def GET(self):
        render = web.template.render('asset', base='before.common', globals=globals())
        return render.register()
    def POST(self):
        i = web.input()
        if i.password2 != i.password:
            flash(_.reg.password_mismatch)
            raise web.redirect('/reg/')
        i.is_public = int('is_public' in i)
        i.is_admin = 0
        i.is_vip = 0
        del i.password2
        r, j = client.post('/users/', data=i)
        if r == codes.created:
            flash(_.reg.ok)
            raise web.redirect('/login/')
        else:
            flash(_.reg.fail)
            raise web.redirect('/reg/')

class User:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            return render.user(user=j)
        else:
            return web.notfound()

class UserEdit:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            return render.user_edit(user=j)
        else:
            return web.notfound()
    def POST(self, id):
        i = web.input()
        i.is_public = int('is_public' in i)
        r, j = client.put('/users/%i/' % int(id), data=i)
        if r == codes.accepted:
            flash(_.user.edit.ok)
            raise web.redirect('/users/%i/' % int(id))
        else:
            flash(_.user.edit.fail)
            raise web.redirect('/users/%i/edit/' % int(id))

class UserFriend:
    def POST(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.post('/users/%i/friends/' % user().user_id, data={'friend_id': int(id)})
        if r == codes.created:
            flash(_.user.friend.ok)
            raise web.redirect('/users/%i/' % int(id))
        else:
            flash(_.user.friend.fail)
            raise web.redirect('/users/%i/' % int(id))

			
class UserBan:
    def POST(self, id, is_banned):
        if not is_admin():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            j.is_banned = int(is_banned)
            r, j = client.put('/users/%i/' % int(id), data=j)
            if r == codes.accepted:
                flash(_.user.ban.ok)
                return web.redirect('/users/%i/' % int(id))
        flash(_.user.ban.fail)
        return web.redirect('/users/%i/' % int(id))

class TopicList:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/')
        if r == codes.ok:
            return render.topics_list(topics=j)
        return web.notfound()

class TopicHotList:
    def GET(self):
        if not is_admin():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/hot/')
        if r == codes.ok:
            return render.topics_list(topics=j)
        else:
            return web.notfound()

class TopicNew:
    def GET(self):
        if not user() or is_banned():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.topics_new()

    def POST(self):
        if not user() or is_banned():
            return web.notfound()
        i = web.input(image={})
        i.user_id = session.user.user_id
        i.is_public = int('is_public' in i)
        i.image_id = os.urandom(16).encode('hex') + os.path.splitext(i.image.filename)[1];
        f = open(image_path(i.image_id), 'wb')
        f.write(i.image.file.read())
        f.close()
        del i.image
        r, j = client.post('/topics/', data=i)
        if r == codes.created:
            flash(_.topic.new.ok)
            raise web.redirect('/topics/%i/' % int(j.topic_id))
        else:
            flash(_.topic.new.fail)
            return web.redirect('/topics/new/')
            
class UserList:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/');
        return render.user_list(user_list=j)

class TopicMy:
    def GET(self):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/topics/' % int(session.user.user_id))
        if r == codes.ok:
            return render.topics_my(topics=j)
        else:
            return web.notfound()
            
class Topic:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/%i/' % int(id))
        if r != codes.ok:
            return web.notfound()
        r, c = client.get('/topics/%i/comments/' % int(id))
        if r != codes.ok:
            return web.notfound()
        return render.topics_detail(topic=j,comments=c)
            
class TopicEdit:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/%i/' % int(id))
        if r == codes.ok:
            return render.topics_edit(topic=j)
        else:
            return web.notfound()
    
    def POST(self, id):
        if not user():
            return web.notfound()
        i = web.input(image={})
        i.user_id = session.user.user_id
        i.is_public = int('is_public' in i)
        i.image_id = os.urandom(16).encode('hex') + os.path.splitext(i.image.filename)[1];
        f = open(image_path(i.image_id), 'wb')
        f.write(i.image.file.read())
        f.close()
        del i.image
        r, j = client.put('/topics/%i/' % int(id), data=i)
        if r == codes.accepted:
            flash(_.topic.edit.ok)
            raise web.redirect('/topics/%i/' % int(id))
        else:
            flash(_.topic.edit.fail)
            return web.redirect('/topics/%i/edit/' % int(id))
    
class TopicDelete:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.delete('/topics/%i/' % int(id))
        if r == codes.ok:
            raise web.redirect('/topics/');
        else:
            return web.notfound()
            
class TopicComment:
    def POST(self, id):
        if not user():
            return web.notfound()
        i = web.input()
        r, j = client.post('/topics/%i/comments/' % int(id), data=i)
        if r == codes.created:
            raise web.redirect('/topics/%i/' % int(id));
        else:
            return web.notfound()

class TopicCommentDelete:
    def POST(self, topic_id, comment_id):
        if not is_admin():
            return web.notfound()
        r, j = client.delete('/topics/%i/comments/%i/' % (int(topic_id), int(comment_id)))
        if r == codes.accepted:
            raise web.redirect('/topics/%i/' % int(topic_id))
        else:
            return web.notfound()

class BanList:
    def GET(self):
        if not is_admin():
            return web.notfound()
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/bans/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipList:
    def GET(self):
        if not is_admin():
            return web.notfound()
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/vips/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipPending:
    def GET(self):
        if not is_admin():
            return web.notfound()
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/vips/pending/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipSet:
    def POST(self, id, is_vip):
        if not is_admin() and int(is_vip) != 2:
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            j.is_vip = int(is_vip)
            r, j = client.put('/users/%i/' % int(id), data=j)
            if r == codes.accepted:
                flash(_.vip.set.ok if int(is_vip != 2) else _.vip.set.up.ok)
                return web.redirect('/users/%i/' % int(id))
        flash(_.vip.set.fail)
        return web.redirect('/users/%i/' % int(id))

class NotificationsNew:
    def GET(self):
        if not is_admin() and not is_vip():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.notifications_new()

    def POST(self):
        if not is_admin() and not is_vip():
            return web.notfound()
        i = web.input()
        i.user_id = session.user.user_id
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.post('/notifications/new/', data=i)
        if r == codes.created:
            flash(_.notification.new.ok)
            raise web.redirect('/notifications/new/')
        else:
            flash(_.notification.new.fail)
            raise web.redirect('/notifications/new/')

class GroupNew:
    def GET(self):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.groups_new()

    def POST(self):
        if not user():
            return web.notfound()
        i = web.input()
        i.user_id = session.user.user_id
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.post('/groups/', data=i)
        if r == codes.created:
            flash(_.group.new.ok)
            raise web.redirect('/groups/%i/' % int(j.group_id))
        else:
            flash(_.group.new.fail)
            raise web.redirect('/groups/new/')

class GroupList:
    def GET(self):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/groups/')
        if r == codes.ok:
            return render.groups_list(groups_list=j)
        return web.notfound()

class GroupMy:
    def GET(self):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/groups/' % int(session.user.user_id))
        if r == codes.ok:
            return render.groups_list(groups_list=j)
        return web.notfound()

class Group:
    def GET(self, id):
        if not user():
            return web.notfound()
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/groups/%i/' % int(id))
        if r == codes.ok:
            return render.groups_detail(group=j)
        return web.notfound()

class GroupJoin:
    def POST(self, group_id):
        i = {'user_id':session.user.user_id}
        r, j = client.post('/groups/%i/requests/' % int(group_id), data=i)
        if r == codes.created:
            #send notifications!!!!
            return web.redirect('/groups/%i/' % int(group_id))

        return web.notfound()

class GroupQuit:
    def POST(self, group_id):
        i = {'user_id':session.user.user_id}
        r, j = client.delete('/groups/%i/' % int(group_id), data=i)
        if r == codes.accepted:
            return web.redirect('/groups/list/')

        return web.notfound()

class GroupApprove:
    def POST(self, group_id, user_id, is_approved):
        i = {'user_id':session.user.user_id}
        if is_approved == 1:
            r, j = client.post('/groups/%i/requests/%i/' % (int(group_id),int(user_id)), data=i)
            if r == codes.created:
                return web.redirect('/groups/requests/')
        elif is_approved == 0:
            r, j = client.delete('/groups/%i/requests/%i/' % (int(group_id),int(user_id)), data=i)
            if r == codes.accepted:
                return web.redirect('/groups/requests/')

        return web.notfound()

class GroupRequests:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/groups/requests/' % session.user.user_id)
        if r == codes.ok:
            return render.groups_requests(requests=j)

        return web.notfound()

class Notifications:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        i = {'user_id':session.user.user_id}
        r, j = client.get('/notifications/', data=i)
        if r == codes.ok:
            return render.notifications_list(notifications=j)

        return web.notfound()

if __name__ == "__main__":
    app.run()