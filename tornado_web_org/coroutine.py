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


# how to call a coroutine
@gen.coroutine
def divide(x, y):
    return x / y

def bad_call():
    divide(1, 0)

@gen.coroutine
def good_call():
    yield divide(1, 0)

from tornado.ioloop import IOLoop
IOLoop.current().spawn_callback(divide, 1, 0)
IOLoop.current().run_sync(lambda: divide(1, ))



## Coroutine patterns
# interaction with callbacks
@gen.coroutine
def call_task():
    yield gen.Task(divide, 1, 0)




# calling blocking functions
thread_pool = ThreadPoolExecutor(4)
@gen.coroutine
def call_blocking():
    yield thread_pool.submit(blocking_func, args)



# Parallelism
@gen.coroutine
def parallel_fetch(url1, url2):
    resp1, resp2 = yield [http_client.fetch(url1),
                          http_client.fetch(url2)]

@gen.coroutine
def parallel_fetch_many(urls):
    responses = yield [http_client.fetch(url) for url in urls]

@gen.coroutine
def parallel_fetch_dict(urls):
    responses = yield {url: http_client.fetch(url) for url in urls}



# Interleaving
@gen.coroutine
def get(self):
    fetch_future = self.fetch_next_chunk()
    while True:
        chunk = yield fetch_future
        if chunk is None: break
        self.write(chunk)
        fetch_future = self.fetch_next_chunk()
        yield self.flush()


# Running in the background
@gen.coroutine
def minute_loop():
    while True:
        yield do_something()
        yield gen.sleep(60)

IOLoop.current().spawn_callback(minute_loop)


# Above loop runs every 60+N seconds where N is the running time of do_sth()
# To run exactly every 60 seconds, use the interleaving pattern from above
@gen.coroutine
def minute_loop2():
    while True:
        nxt = gen.sleep(60)
        yield do_something()
        yield nxt