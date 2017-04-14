import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world!")
        self.write('<a href="%s%>link to story 1</a>' % self.reverse_url("story", "1"))


class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write("This is story %s" % story_id)


def make_app():
    return tornado.web.Application([
        tornado.web.url(r"/", MainHandler),
        tornado.web.url(r"/story/([0-9]+)", StoryHandler, name="story")
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
