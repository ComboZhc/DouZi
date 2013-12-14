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
    r'/users/','UserList',
    r'/users/(\d+)/ban/(\d+)/','UserBan',
    r'/users/(\d+)/', 'User',
    r'/users/(\d+)/edit/?', 'UserEdit',
    r'/topics/','TopicList',
    r'/topics/new/?', 'TopicNew',
    r'/topics/my/','MyTopics',
    r'/topics/(\d+)/','Topic',
    r'/topics/(\d+)/edit/?', 'TopicEdit',
    r'/topics/(\d+)/delete/?', 'TopicDelete',
    r'/topics/(\d+)/comments/', 'TopicComment',
    r'/bans/', 'BanList',
    r'/vips/', 'VipList',
    r'/vips/pending/', 'VipPending',
    r'/vips/(\d+)/(\d+)/','VipSet',
)
app = web.application(urls, globals())

web.config.debug = True

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
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            return render.user(user=j)
        else:
            return web.notfound()

class UserEdit:
    def GET(self, id):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r == codes.ok:
            return render.user_edit(user=j)
        else:
            return web.notfound()
    def POST(self, id):
        i = web.input()
        i.is_public = int('is_public' in i)
        i.is_vip = session.user.is_vip
        r, j = client.put('/users/%i/' % int(id), data=i)
        if r == codes.ok:
            flash(_.user.edit.ok)
            raise web.redirect('/users/%i/' % int(id))
        else:
            flash(_.user.edit.fail)
            raise web.redirect('/users/%i/edit/' % int(id))
			
class UserBan:
    def GET(self, id, is_banned):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/' % int(id))
        if r != codes.ok:
            return web.redirect('/users/%i/' % int(id))
        j.is_banned = int(is_banned)
        r, j = client.put('/users/%i/' % int(id), data=j)
        return web.redirect('/users/%i/' % int(id))

class TopicList:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/')
        print r, j
        if r == codes.ok:
            return render.topics_list(topics=j)
        else:
            return web.notfound()

class TopicNew:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.topics_new()
    def POST(self):
        i = web.input(image={})
        i.user_id = session.user.user_id
        i.is_public = int('is_public' in i)
        i.image_id = os.urandom(16).encode('hex') + os.path.splitext(i.image.filename)[1];
        f = open(image_path(i.image_id), 'wb')
        f.write(i.image.file.read())
        f.close()
        del i.image
        r, j = client.post('/topics/', data=i)
        if r == codes.ok:
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

class MyTopics:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/users/%i/topics/' % int(session.user.user_id))
        if r == codes.ok:
            return render.topics_my(topics=j)
        else:
            return web.notfound()
            
class Topic:
    def GET(self, id):
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
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/%i/' % int(id))
        if r == codes.ok:
            return render.topics_edit(topic=j)
        else:
            return web.notfound()
    
    def POST(self, id):
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
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.delete('/topics/%i/' % int(id))
        if r == codes.ok:
            raise web.redirect('/topics/');
        else:
            return web.notfound()
            
class TopicComment:
    def POST(self, id):
        r, j = client.post('/topics/%i/comments/' % int(id))
        if r == codes.ok:
            raise web.redirect('/topics/%i/' % int(id));
        else:
            return web.notfound()

class BanList:
    def GET(self):
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/bans/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipList:
    def GET(self):
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/vips/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipPending:
    def GET(self):
        render = web.template.render('asset',base='after.common', globals=globals())
        r, j = client.get('/vips/pending/')
        if r == codes.ok:
            return render.user_list(user_list=j)
        else:
            return web.notfound()

class VipSet:
    def GET(self, id, is_vip):
        render = web.template.render('asset', base='after.common', globals=globals())
        v = int(is_vip)
        r, j = client.get('/users/%i/' % int(id))
        if r != codes.ok:
            return web.notfound()
        if session.user.is_admin or session.user.user_id == int(id) and v == 2:
            j.is_vip = v
            r, j = client.put('/users/%i/' % int(id), data=j)
            if r == codes.accepted:
                flash(_.vip.set.ok)
                return web.redirect('/users/%i/' % int(id))
            else:
                flash(_.vip.set.ok)
                return web.redirect('/users/%i/' % int(id))
        else:
            flash(_.vip.set.ok)
            return web.redirect('/users/%i/' % int(id))

if __name__ == "__main__":
    app.run()