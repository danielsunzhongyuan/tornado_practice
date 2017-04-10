# coding=utf-8
import tornado.options
import tornado.web
import tornado.ioloop
import tornado.httpserver

import pymongo

from tornado.options import options, define

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        conn = pymongo.MongoClient()
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            # 从字典中删除_id键（以便Python的json库可以将其序列化）
            # 因为 word_doc["_id"] 是一个 ObjectId 对象
            # "_id" : ObjectId("58eb2038378ef32cc8a63527")
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

    def post(self, word):
        definition = self.get_argument("definition")
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            word_doc['definition'] = definition
            coll.save(word_doc)
        else:
            word_doc = {'word': word, 'definition': definition}
            coll.insert(word_doc)
        del word_doc["_id"]
        self.write(word_doc)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
