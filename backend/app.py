import web
from requests import codes
import sqlite3
import json

urls = (
    r'/?', 'Home',
    r'/login/', 'Login',
    r'/logout/', 'Logout',
)

app = web.application(urls, globals())

web.config.debug = True

con = sqlite3.connect("test.db")
cur = con.cursor()
cur.executescript('''
    CREATE TABLE IF NOT EXISTS User
    (
        id INTEGER PRIMARY KEY ASC,
        username TEXT,
        password TEXT,
        is_vip INTEGER,
        is_banned INTEGER,
        is_admin INTEGER,
        is_public INTEGER
    );
    '''
    )

class Login:

    def POST(self):
        i = json.loads(web.input().keys()[0])
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM User where username=:u and password=:p", {'u':i['username'], 'p':i['password']})
        r = cur.fetchone()
        if r == None:
            raise web.unauthorized()
        else:
            j = {
                'id': r['id'],
                'is_vip': r['is_vip'],
                'is_banned': r['is_banned'],
                'is_admin': r['is_admin'],
                'is_public': r['is_public'],
            }
            return json.dumps(j)

class Logout:
    def GET(self):
        session.user = {}
        session.username = ''
        session.message = ''
        session.kill()
        raise web.redirect("/")

            
if __name__ == "__main__":
    app.run()