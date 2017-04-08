import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class NowaMagicHandler(tornado.web.RequestHandler):
    def get(self):
        content = u'Welcome to NowaMagic.'
        self.render("index.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/nowamagic/", NowaMagicHandler),
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
