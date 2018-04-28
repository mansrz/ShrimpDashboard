import tornado.ioloop
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class MetricHandler(BaseHandler):
    def get(self):
        return None

    def post(self):
        session = self.get_secure_cookie("user")
        if(session is not None):
            print(self.get_argument("id"))
        else:
            self.send_error()


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

settings = {
    "cookie_secret": "0ELiVte7oKPjnXtggELRC3MpOcCokFf8",
    "login_url": "/login",
}
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/metric", MetricHandler),
        (r"/login", LoginHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
