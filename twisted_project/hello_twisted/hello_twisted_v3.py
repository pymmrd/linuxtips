# -*- coding:utf-8 -*-

"""
如下一段代码，看看阻塞的效果。在开始的时候运行一个打印任务，
非阻塞，然后1秒之后，发送一个指向google的请求，到第3秒的
时候，再执行打印。
Hello world!===>yudahai===>1546233313
Unhandled Error
Traceback (most recent call last):
  File "hello_twisted_v3.py", line 27, in <module>
    reactor.run()
  File "/usr/lib/python2.7/dist-packages/twisted/internet/base.py", line 1192, in run
    self.mainLoop()
  File "/usr/lib/python2.7/dist-packages/twisted/internet/base.py", line 1201, in mainLoop
    self.runUntilCurrent()
--- <exception caught here> ---
  File "/usr/lib/python2.7/dist-packages/twisted/internet/base.py", line 824, in runUntilCurrent
    call.func(*call.args, **call.kw)
  File "hello_twisted_v3.py", line 19, in request_google
    res = requests.get('http://www.google.com')
  File "/usr/lib/python2.7/dist-packages/requests/api.py", line 55, in get
    return request('get', url, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 455, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/sessions.py", line 558, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/dist-packages/requests/adapters.py", line 378, in send
    raise ConnectionError(e)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='www.google.com', port=80): Max retries exceeded with url: / (Caused by <class 'socket.error'>: [Errno 110] Connection timed out)

Hello world!===>yuyue===>1546233441

看看第一个打印和第三个打印之间相隔128秒，这个程序什么事都没干，仅仅是等待。解决方案hello_twisted_v4.py

"""


import time
import requests
from twisted.internet import reactor, task


def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))


def request_google():
    res = requests.get('http://www.google.com')
    return res


if __name__ == "__main__":
    reactor.callWhenRunning(hello, 'yudahai')
    reactor.callLater(1, request_google)
    reactor.callLater(3, hello, 'yuyue')
    reactor.run()
