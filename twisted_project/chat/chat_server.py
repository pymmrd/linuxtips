# -*- coding:utf-8 -*-

"""
    Chat继承LineReceive，而LineReceive继承Protocol的。真实的连接是transport，
所以我们这个例子中没有展示出来transport，只有sendLine这样的函数，我下面自己写
例子的时候，会加上去；
    Protocol其实就是整个连接连上来以后，加上一些这个连接当前的状态，再加上一些
基本操作方法组成的；
    Factory就是所有Protocol组成的一个工厂类，每新加入或者减少一个Protocol对象时，
都能在Factory里面表现出来。
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        """
        连接创建好以后，触发的函数
        """
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        """
        连接丢失以后，触发的函数，这个函数以后
        可以扩展到redis记录连接状态
        """
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        """
        这个是一个连接用的最多的函数，就是数据接受到
        以后，触发的函数
        """
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        """
        当state在未验证状态时，调用handle_GETNAME函数
        """
        if name in self.users:
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        """
        当已经验证过时，调用handle_CHAT
        """
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):
    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        """
        新建一个连接以后，触发的函数，它调用了Chat的构造函数，
        新建一个Chat对象
        """
        return Chat(self.users)

reactor.listenTCP(8123, ChatFactory())
reactor.run()
