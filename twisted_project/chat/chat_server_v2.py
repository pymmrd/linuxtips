# -*- coding:utf-8 -*-

"""
    数据模型，官方例子很简单，直接把str格式的数据发送出去，在测试的时候没问题，
但正式项目中绝对不可能。通常每个数据，都会由2部分组成，一个header作为头，一个
content作为内容。其实就是模拟http。header中，通常有数据长度、版本号、数据类型
id等，这个都不是必须的，要根据你实际项目来。content作为真实数据内容，一般都用
json数据格式，当然，如果你追求效率，也可以用google protor buf或者facebook的数
据模式，都可以(很多公司都用的google protor buf模式，解析速度比较快，我们这为了
简单，就用json格式)。
    数据格式如下:
    -----------------------------------------------------------------------------
    |length              | version          |command_id        |content          |
    -----------------------------------------------------------------------------
    header字段: length, version, command_id
    content: content

    comamnd_id解释:
        类似于http中的url，http根据url表明它的作用, 我们这同样根据command_id标示它的
        作用，因为在整个过程中，不但有聊天，还有验证过程，以后还可能有广播，组播等各
        种功能。我们就根据command_id来判断这个数据的作用(其实写到这，大家完全可以看出
        来，我们基本就是跟http学的，现实过程中也这样，几乎都在模仿http)，而响应之类的，
        就是服务器主动推送给客户端的command_id，这也是跟http不同的地方，很多时候，我们
        都是主动推送给客户端。

　　    好了，既然已经这样规定，我们再详细规定一下command_id吧，就像http的url一样。
        -----------------------------------------------------------------------
        |command_id                        | 作用                              |
        -----------------------------------------------------------------------
        |1                                 |               验证                |
        -----------------------------------------------------------------------
        |2                                 |               单聊                |
        -----------------------------------------------------------------------
        |3                                 |               组播                |
        -----------------------------------------------------------------------
        |4                                 |               广播                |
        -----------------------------------------------------------------------
        |101                               |               响应验证            |
        -----------------------------------------------------------------------
        |102                               |               响应单聊            |
        -----------------------------------------------------------------------
        |103                               |               响应组播            |
        -----------------------------------------------------------------------
        |104                               |               响应广播            |
        -----------------------------------------------------------------------

开启服务端:
$ python chat_server_v2.py 
2019-01-01 15:22:41+0800 [-] Log opened.
2019-01-01 15:22:41+0800 [-] ChatFactory starting on 8124
2019-01-01 15:22:41+0800 [-] Starting factory <__main__.ChatFactory instance at 0x7f2123f35f80>
2019-01-01 15:22:58+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44513)
2019-01-01 15:23:01+0800 [Chat,0,127.0.0.1] 欢迎, 000001!
2019-01-01 15:23:08+0800 [Chat,0,127.0.0.1] Phone_number:000003 不在线,不能聊天.
2019-01-01 15:23:09+0800 [Chat,0,127.0.0.1] Phone_number:000004 不在线,不能聊天.
2019-01-01 15:23:09+0800 [Chat,0,127.0.0.1] Phone_number:000002 不在线,不能聊天.
2019-01-01 15:23:10+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44515)
2019-01-01 15:23:13+0800 [Chat,1,127.0.0.1] 欢迎, 000002!
2019-01-01 15:23:20+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44516)
2019-01-01 15:23:20+0800 [Chat,1,127.0.0.1] Phone_number:000003 不在线,不能聊天.
2019-01-01 15:23:21+0800 [Chat,1,127.0.0.1] Phone_number:000003 不在线,不能聊天.
2019-01-01 15:23:21+0800 [Chat,1,127.0.0.1] Phone_number:000003 不在线,不能聊天.
2019-01-01 15:23:23+0800 [Chat,2,127.0.0.1] 欢迎, 000003!
2019-01-01 15:23:31+0800 [Chat,2,127.0.0.1] Phone_number:000004 不在线,不能聊天.
2019-01-01 15:23:31+0800 [Chat,2,127.0.0.1] Phone_number:000004 不在线,不能聊天.
2019-01-01 15:29:42+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44562)
2019-01-01 15:29:45+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44563)
2019-01-01 15:29:45+0800 [Chat,3,127.0.0.1] 欢迎, 000001!
2019-01-01 15:29:47+0800 [__main__.ChatFactory] New connection, the info is: IPv4Address(TCP, '127.0.0.1', 44564)
2019-01-01 15:29:48+0800 [Chat,4,127.0.0.1] 欢迎, 000002!
2019-01-01 15:29:50+0800 [Chat,5,127.0.0.1] 欢迎, 000003!


开启三个客户端:
$ python chat_client.py 000001
2019-01-01 15:29:42+0800 [-] Log opened.
2019-01-01 15:29:42+0800 [-] Starting factory <__main__.EchoClientFactory instance at 0x7f6f19a8c8c0>
2019-01-01 15:29:42+0800 [-] Started to connect
2019-01-01 15:29:42+0800 [Uninitialized] Connected.
2019-01-01 15:29:42+0800 [Uninitialized] New connection IPv4Address(TCP, '127.0.0.1', 8124)
2019-01-01 15:29:45+0800 [EchoClient,client] 验证通过
2019-01-01 15:29:54+0800 [EchoClient,client] [群聊][000001]:你好,这是群聊
2019-01-01 15:29:55+0800 [EchoClient,client] [单聊][000002]:你好,这是单聊
2019-01-01 15:29:57+0800 [EchoClient,client] [群聊][000002]:你好,这是群聊
2019-01-01 15:29:57+0800 [EchoClient,client] [单聊][000003]:你好,这是单聊
2019-01-01 15:29:59+0800 [EchoClient,client] [群聊][000003]:你好,这是群聊

$python chat_client.py 000002
2019-01-01 15:29:45+0800 [-] Log opened.
2019-01-01 15:29:45+0800 [-] Starting factory <__main__.EchoClientFactory instance at 0x7efd7dc2d8c0>
2019-01-01 15:29:45+0800 [-] Started to connect
2019-01-01 15:29:45+0800 [Uninitialized] Connected.
2019-01-01 15:29:45+0800 [Uninitialized] New connection IPv4Address(TCP, '127.0.0.1', 8124)
2019-01-01 15:29:48+0800 [EchoClient,client] 验证通过
2019-01-01 15:29:52+0800 [EchoClient,client] [单聊][000001]:你好,这是单聊
2019-01-01 15:29:53+0800 [EchoClient,client] [组聊][000001]:你好,这是组聊
2019-01-01 15:29:54+0800 [EchoClient,client] [群聊][000001]:你好,这是群聊
2019-01-01 15:29:57+0800 [EchoClient,client] [群聊][000002]:你好,这是群聊
2019-01-01 15:29:58+0800 [EchoClient,client] [组聊][000003]:你好,这是组聊
2019-01-01 15:29:59+0800 [EchoClient,client] [群聊][000003]:你好,这是群聊

$python chat_client.py 000003
2019-01-01 15:29:47+0800 [-] Log opened.
2019-01-01 15:29:47+0800 [-] Starting factory <__main__.EchoClientFactory instance at 0x7f38c8ece8c0>
2019-01-01 15:29:47+0800 [-] Started to connect
2019-01-01 15:29:47+0800 [Uninitialized] Connected.
2019-01-01 15:29:47+0800 [Uninitialized] New connection IPv4Address(TCP, '127.0.0.1', 8124)
2019-01-01 15:29:50+0800 [EchoClient,client] 验证通过
2019-01-01 15:29:53+0800 [EchoClient,client] [组聊][000001]:你好,这是组聊
2019-01-01 15:29:54+0800 [EchoClient,client] [群聊][000001]:你好,这是群聊
2019-01-01 15:29:56+0800 [EchoClient,client] [组聊][000002]:你好,这是组聊
2019-01-01 15:29:57+0800 [EchoClient,client] [群聊][000002]:你好,这是群聊
2019-01-01 15:29:59+0800 [EchoClient,client] [群聊][000003]:你好,这是群聊
"""

# StdLib imports
import sys
import json
import struct

# Twisted imports
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.python import log

log.startLogging(sys.stdout)

class Chat(Protocol):
    """
　  首先，直接从Protocol继承了，这样比从LineReceive继承更直观一点；command_func_dict
    代表command_id和其处理函数的一一对应字典;

　  其次，dataReceived是主要的接受函数，接受到数据以后，先解析header，根据header里面
    的length截取数据，再根据command_id来把数据送个它的处理函数。如果command_id为1，就
    进入验证函数；如果为其他，就进入其他数据处理函数，不过要先验证通过，才能用其他函数
    处理。这就跟http一样。(这边以后要重写的，大家想象一下，如果我一个客户端连接，同时
    发送2个数据，按照上面代码，只能处理一个数据，另外一个就丢弃了。)

　  最后，send_content为总的发送函数，先把header头组建好，然后加上数据，就发送了。这边
    可能遇到发送的客户端不在线，要先检测一下(以后还会遇到各种意外断线情况，服务器端没法
    及时检测到，这个以后再讲。)
    """
    def __init__(self, users):
        self.users = users
        self.phone_number = None
        self.state = "VERIFY"
        self.version = 0
        self.command_func_dict = {
            1: self.handle_verify,
            2: self.handle_single_chat,
            3: self.handle_group_chat,
            4: self.handle_broadcast_chat
        }

    def connectionMade(self):
        log.msg("New connection, the info is:", self.transport.getPeer())

    def connectionLost(self, reason):
        if self.phone_number in self.users:
            del self.users[self.phone_number]

    def dataReceived(self, data):
        """
        接受到数据以后的操作
        """
        length, self.version, command_id = struct.unpack('!3I', data[:12])
        content = data[12:length]

        if command_id not in [1, 2, 3, 4]:
            return

        if self.state == "VERIFY" and command_id == 1:
            self.handle_verify(content)
        else:
            self.handle_data(command_id, content)

    def handle_verify(self, content):
        """
        验证函数
        """
        content = json.loads(content)
        phone_number = content.get('phone_number')
        if phone_number in self.users:
            log.msg("电话号码<%s>存在老的连接." % phone_number.encode('utf-8'))
            self.users[phone_number].connectionLost("")
        log.msg("欢迎, %s!" % (phone_number.encode('utf-8'),))
        self.phone_number = phone_number
        self.users[phone_number] = self
        self.state = "DATA"

        send_content = json.dumps({'code': 1})

        self.send_content(send_content, 101, [phone_number])

    def handle_data(self, command_id, content):
        """
        根据command_id来分配函数
        """
        self.command_func_dict[command_id](content)

    def handle_single_chat(self, content):
        """
        单播
        """
        content = json.loads(content)
        chat_from = content.get('chat_from')
        chat_to = content.get('chat_to')
        chat_content = content.get('chat_content')
        send_content = json.dumps(
            dict(
                chat_from=chat_from,
                chat_content=chat_content
            )
        )

        self.send_content(send_content, 102, [chat_to])

    def handle_group_chat(self, content):
        """
        组播
        """
        content = json.loads(content)
        chat_from = content.get('chat_from')
        chat_to = content.get('chat_to')
        chat_content = content.get('chat_content')
        send_content = json.dumps(
            dict(
                chat_from=chat_from,
                chat_content=chat_content
            )
        )
        phone_numbers = chat_to
        self.send_content(send_content, 103, phone_numbers)

    def handle_broadcast_chat(self, content):
        """
        广播
        """
        content = json.loads(content)
        chat_from = content.get('chat_from')
        chat_content = content.get('chat_content')
        send_content = json.dumps(
            dict(chat_from=chat_from, chat_content=chat_content)
        )
        phone_numbers = self.users.keys()
        self.send_content(send_content, 104, phone_numbers)

    def send_content(self, send_content, command_id, phone_numbers):
        """
        发送函数
        """
        length = 12 + len(send_content)
        version = self.version
        command_id = command_id
        header = [length, version, command_id]
        header_pack = struct.pack('!3I', *header)
        for phone_number in phone_numbers:
            if phone_number in self.users.keys():
                self.users[phone_number].transport.write(header_pack + send_content)
            else:
                log.msg("Phone_number:%s 不在线,不能聊天." % phone_number.encode('utf-8'))


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(8124, ChatFactory())
reactor.run()
