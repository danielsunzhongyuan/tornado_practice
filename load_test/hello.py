import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

import json
import MySQLdb

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        # response = client.fetch("http://www.baidu.com")
        self.write("success")


class AsyncIndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("http://www.baidu.com", callback=self.on_response)

    def on_response(self, response):
        self.write("success")
        self.finish()


class AsyncGenIndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, "http://www.baidu.com")
        self.write("success")
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/index", IndexHandler),
        (r"/index_async", AsyncIndexHandler),
        (r"/index_async_gen", AsyncGenIndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
