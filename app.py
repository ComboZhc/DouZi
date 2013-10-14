import web
import client
from requests import codes
import _
import os

urls = (
    r'/?', 'TopicList',
    r'/login/?', 'Login',
    r'/logout/?', 'Logout',
    r'/reg/?', 'Reg',
    r'/users/(\d+)/?', 'User',
    r'/users/(\d+)/edit/?', 'UserEdit',
    r'/topics/new/?', 'TopicNew',
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
    return os.path.join('static', 'images', filename)


class Home:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.dashboard()

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
        i.is_public = int(bool(i.is_public))
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
        r, j = client.put('/users/%i/' % int(id), data=i)
        if r == codes.accepted:
            flash(_.user.edit.ok)
            raise web.redirect('/users/%i/' % int(id))
        else:
            flash(_.user.edit.fail)
            raise web.redirect('/users/%i/edit/' % int(id))

class TopicList:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        r, j = client.get('/topics/')
        if r == codes.ok:
            return render.dashboard(dashboard=j)
        else:
            return web.notfound()

class TopicNew:
    def GET(self):
        render = web.template.render('asset', base='after.common', globals=globals())
        return render.topic_new()
    def POST(self):
        i = web.input(image={})
        i.is_public = int('is_public' in i)
        i.image_id = os.urandom(16).encode('hex')
        f = open(image_path('%s%s' % (i.image_id, os.path.splitext(i.image.filename)[1])), 'w')
        f.write(i.image.file.read())
        f.close()
        del i.image
        r, j = client.post('/topics/', data=i)
        if r == codes.created:
            flash(_.topic.new.ok)
            raise web.redirect('/topics/%i/' % j.topic_id)
        else:
            flash(_.topic.new.fail)
            return web.redirect('/topics/new')

if __name__ == "__main__":
    app.run()