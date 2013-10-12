import web
urls = (
    '/', 'Home',
    '/login/', 'Login',
    '/logout/', 'Logout',
)
app = web.application(urls, globals())

session = None
if web.config.get('_session') is None:
    session = web.session.Session(app, 
        web.session.DiskStore('.sessions'), 
        initializer = {
            'userid': -1,
            'username': None,
        }
    )
    web.config._session = session
else:
    session = web.config._session

class Home:
    def GET(self):
        return 'Hello, %s!' % session.username

class Login:        
    def GET(self):
        render = web.template.render('asset')
        return render.login()

    def POST(self):
        i = web.input()
        session.username = i.username
        session.userid = 1
        raise web.seeother("/")

class Logout:
    def GET(self):
        pass


if __name__ == "__main__":
    app.run()