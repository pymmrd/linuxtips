# -*- coding:utf-8 -*-

"""
  实际过程中，访问数据库，访问网络，都有可能阻塞住。程序一旦阻塞，效率会极其底下。
  这边有2种方法:
    1. 用twisted自带的httpclient进行访问，twisted自带的httpclient
       由于是异步的，不会阻塞住整个reactor的运行
    2. 用线程的方式运行，注意，这里的线程不是python普通线程，
       是twisted自带的线程，它访问完毕的时候，会发送一个信号给reactor。
  输出如下:
    Hello world!===>yudahai===>1546320993
    Hello world!===>yuyue===>1546320996
    User timeout caused connection failure
"""

import time
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, task, defer


def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))


@defer.inlineCallbacks
def request_google():
    agent = Agent(reactor)
    try:
        result = yield agent.request(
            'GET',
            'http://www.google.com',
             Headers({'User-Agent': ['Twisted Web Client Example']}),
             None
        )
    except Exception as e:
        print e
        return 
    print(result)


if __name__ == '__main__':
    reactor.callWhenRunning(hello, 'yudahai')
    reactor.callLater(1, request_google)
    reactor.callLater(3, hello, 'yuyue')
    reactor.run()
