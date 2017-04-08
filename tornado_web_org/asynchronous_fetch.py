# synchronous version
from tornado.httpclient import HTTPClient
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body



# asynchronous version with callback
from tornado.httpclient import AsyncHTTPClient
def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)


from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result())
    )
    return my_future


from tornado import gen
from tornado.httpclient import AsyncHTTPClient
@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    # in Python versions prior to 3.3
    raise gen.Return(response.body)
    # in Python versions after 3.3
    # return response.body




