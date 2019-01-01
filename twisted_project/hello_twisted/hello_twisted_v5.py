# -*- coding:utf-8 -*-

"""
    在现实过程中，我们很多库没有非阻塞模式的api，要非阻塞模式，
    一定要返回twisted的defer对象，如果写一个库，还要针对twisted
    写一个异步版，这肯定强人所难。而且很多时候，哪怕自己的函数，
    如果不是特别复杂，都可以用线程模式，twisted本身访问数据库
    就是线程模式。我们来看看线程模式的代码。
    输出如下:
        Hello world!===>yudahai===>1546321214
        Hello world!===>yuyue===>1546321217
        (<urllib3.connectionpool.HTTPConnectionPool object at 0x7fcfe7eb99d0>, 'Connection to www.google.com timed out. (connect timeout=10)')
    大家可能会在想，既然线程也可以把阻塞代码线程化，为啥还直接写异步代码呢？
    异步代码那么难写、难看还容易出错。
    　　这边其实有几个理由，在twisted中，不能大量使用线程。
    　　1、效率问题，如果用线程，我们干嘛还用twisted呢？线程会频繁切换cpu调度，
           如果大量使用线程，会极大浪费cpu资源，效率会严重下降。
    　　2、线程安全，如果第一个问题稍微还有点理由的话，那线程安全问题绝对不能忽视了。
           比如用twisted接受网络数据的时候，是非线程安全的，如果用线程模式接受数据，
           会引起程序崩溃。twisted只有极少数的api支持线程。其实用的最多的例子就是消
           息队列的接受系统，很多初级程序员会用线程模式来做消息队列的接受方式，一开始
           没问题，结果运行一段时间以后，就会发现程序不能正常接受数据了，而且还不报错
           twisted官方也建议大家，只要有异步库，一定优先使用异步库，线程只是做非常简
           单而且不是频繁的操作。
"""

import time
import requests
from twisted.internet import reactor, task, defer


def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))


def request_google():
    try:
        result = requests.get('http://www.google.com', timeout=10)
    except Exception as e:
        print e
        return 
    print(result)


if __name__ == '__main__':
    reactor.callWhenRunning(hello, 'yudahai')
    reactor.callInThread(request_google)
    reactor.callLater(3, hello, 'yuyue')
    reactor.run()
