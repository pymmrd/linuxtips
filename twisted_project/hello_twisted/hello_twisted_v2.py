# -*- coding:utf-8 -*-

"""
程序运行结果:
Hello world!===>ding===>1546232818
Hello world!===>yudahai===>1546232818
Hello world!===>yuyue===>1546232821
Hello world!===>ding===>1546232828
Hello world!===>ding===>1546232838
Hello world!===>ding===>1546232848
Hello world!===>ding===>1546232858
Hello world!===>ding===>1546232868
"""


import time
from twisted.internet import reactor, task

def hello(name):
    print("Hello world!===>" + name + '===>' + str(int(time.time())))


if __name__ == '__main__':
    #一个循环任务taks1，task1每10秒运行一次
    task1 = task.LoopingCall(hello, 'ding')
    task1.start(10)

    reactor.callWhenRunning(hello, 'yudahai')
    reactor.callLater(3, hello, 'yuyue')

    reactor.run()
