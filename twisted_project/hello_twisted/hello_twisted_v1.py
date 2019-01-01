# -*- coding:utf-8 -*-

"""
Hello world!===>1546233012
Hello world!===>1546233015
"""


import time
from twisted.internet import reactor

def hello():
    print("Hello world!===>" + str(int(time.time())))

if __name__ == "__main__":
    reactor.callWhenRunning(hello)
    reactor.callLater(3, hello)
    reactor.run()
