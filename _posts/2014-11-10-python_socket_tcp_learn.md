---
layout: post
title: "python实现socket通讯(TCP)"
categories: python 
tags: [python socket]
date: 2014-11-10 21:33:18
---


Server：

{% highlight bash %}
# server

import socketG

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.bind(address)
s.listen(5)

ss, addr = s.accept()
print 'got connected from',addr

ss.send('byebye')
ra = ss.recv(512)
print ra

ss.close()
s.close()

{% endhighlight %}

Client：

{% highlight bash %}
# client

import socket

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

data = s.recv(512)
print 'the data received is',data

s.send('hihi')

s.close()

{% endhighlight %}


<span style="font-size:14px;">&nbsp;&nbsp;</span></p><p><span style="font-size:14px;">&nbsp;</span></p><p><strong><span style="font-size:14px;">运行结果：</span></strong></p><p><strong><span style="font-size:14px;">server</span></strong></p><p><span style="font-size:14px;">[work@db-testing python]$ python server.py <br />got connected from ('127.0.0.1', 47872)<br />hihi</span></p><p><span style="font-size:14px;">&nbsp;</span></p><p><strong><span style="font-size:14px;">client</span></strong></p><p><span style="font-size:14px;">[work@db-testing python]$ python client.py <br />the data received is byebye</span></p><p><span style="font-size:14px;">&nbsp;</span></p><p><span style="font-size:14px;">==============================================================================</span></p><p></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><strong><span style="font-size:14px;">一、套接字</span></strong></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">套接字是为特定网络协议（例如TCP/IP，ICMP/IP，UDP/IP等）套件对上的网络应用程序提供者提供当前可移植标准的对象。它们允许程序接受并进行连接，如发送和接受数据。为了建立通信通道，网络通信的每个端点拥有一个套接字对象极为重要。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">套接字为BSD UNIX系统核心的一部分，而且他们也被许多其他类似UNIX的操作系统包括Linux所采纳。许多非BSD UNIX系统（如ms-dos，windows，os/2，mac os及大部分主机环境）都以库形式提供对套接字的支持。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">三种最流行的套接字类型是:stream, datagram<span style="color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;">,&nbsp;</span>raw。stream和datagram套接字可以直接与TCP协议进行接口，而raw套接字则接口到IP协议。但套接字并不限于TCP/IP。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><strong><span style="font-size:14px;">二、套接字模块</span></strong></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">套接字模块是一个非常简单的基于对象的接口，它提供对低层BSD套接字样式网络的访问。使用该模块可以实现客户机和服务器套接字。要在python 中建立具有TCP和流套接字的简单服务器，需要使用socket模块。利用该模块包含的函数和类定义，可生成通过网络通信的程序。一般来说，建立服务器连 接需要六个步骤。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第1步</strong>是创建socket对象。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">调用socket构造函数。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">socket=socket.socket(familly, type)</span></p><p style="box-sizing: border-box; font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size: 14px;"><span style="color:#4b4b4b;">family的值可以是AF_UNIX(Unix域，用于同一台机器上的进程间通讯)，也可以是AF_INET（对于IPV4协议的TCP和 UDP）或</span><span style="background-color: rgb(255, 255, 255);"> <span style="font-family: simsun; font-size: 16px; line-height: 24px;">AF_INET6（对于IPV6）</span></span><span style="color:#4b4b4b;">，至于type参数，SOCK_STREAM（流套接字）或者 SOCK_DGRAM（数据报文套接字）,SOCK_RAW（raw套接字）。</span></span></p><p style="box-sizing: border-box; font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size: 14px; background-color: rgb(255, 255, 255);"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-family: simsun; font-size: 16px;"><span style="word-wrap: normal; word-break: normal;"><span style="color:#cc0000;">注解：</span>ai_family</span>参数指定调用者期待返回的套接口地址结构的类型。</span><span style="font-family: simsun; font-size: 14px; line-height: 21px;"></span></span></p><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">它的值<span style="word-wrap: normal; word-break: normal;">包括三种：<span style="color:#3333ff;">AF_INET，AF_INET6<span style="font-family: simsun; font-size: 16px; line-height: 24px;">，</span>AF_UNSPEC</span></span></span></div><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">如果指定AF_INET，那么函数就不能返回任何IPV6相关的地址信息；</span></div><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">如果仅指定了AF_INET6，则就不能返回任何IPV4地址信息。</span></div><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">AF_UNSPEC则意味着函数返回的是适用于指定主机名和服务名且适合任何协议族的地址。</span></div><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">如果某个主机既有AAAA记录(IPV6)地址，同时又有A记录(IPV4)地址，那么AAAA记录将作为sockaddr_in6结构返回，而A记录则作为sockaddr_in结构返回。</span><div><div><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">AF_INET6用于IPV6的系统里面，AF_INET 及 PF_INET 是IPV4用的.</span></div></div><div><div><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">AF 表示ADDRESS FAMILY 地址族</span></div><div><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">PF 表示PROTOCOL FAMILY 协议族</span></div></div></div><div style="font-family: simsun; font-size: 14px; line-height: 21px;"><span style="word-wrap: normal; word-break: normal; line-height: 24px; font-size: 16px;">在<span style="word-wrap: normal; word-break: normal;">windows中AF_INET与PF_INET完全一样</span>，而在Unix/Linux系统中，在不同的版本中这两者有微小差别。</span></div><p></p><p style="box-sizing: border-box; font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size: 14px;"><span style="color:#4b4b4b;"><br /></span></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第2步</strong>则是将socket绑定（指派）到指定地址上，socket.bind(address)</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">address必须是一个双元素元组,((host,port)),主机名或者ip地址+端口号。如果端口号正在被使用或者保留，或者主机名或ip地址错误，则引发socke.error异常。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第3步</strong>，绑定后，必须准备好套接字，以便接受连接请求。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">socket.listen(backlog)</span></p><p style="box-sizing: border-box; font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size: 14px;"><span style="color:#3333ff;">backlog指定了最多连接数</span><span style="color:#4b4b4b;">，至少为1，接到连接请求后，这些请求必须排队，如果队列已满，则拒绝请求。</span></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第4步</strong>，服务器套接字通过socket的accept方法等待客户请求一个连接：</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">connection,address=socket.accept()</span></p><p style="box-sizing: border-box; font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size: 14px;"><span style="color:#4b4b4b;">调用accept方法时，socket会进入'waiting'（或阻塞）状态。客户请求连接时，方法建立连接并返回服务器。</span><span style="color:#3333ff;">accept方法返回 一个含有俩个元素的元组，形如(connection, address)</span><span style="color:#4b4b4b;">。第一个元素（connection）是新的socket对象，服务器通过它与客 户通信；第二个元素（address）是客户的internet地址。</span></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第5步</strong>是处理阶段，服务器和客户通过send和recv方法通信（传输数据）。服务器调用send，并采用字符串形式向客户发送信息。send方法返回已发送的字符个数。服务器使用recv方法从客户接受信息。调用recv时，必须指定一个整数来控制本次调用所接受的最大数据量。recv方法在接受数据时会进入'blocket'状态，最后返回一个字符串，用它来表示收到的数据。如果发送的量超过recv所允许，数据会被截断。多余的数据将缓冲于接受端。以后调用recv时，多余的数据会从缓冲区删除。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><strong>第6步</strong>，传输结束，服务器调用socket的close方法以关闭连接。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">建立一个简单客户连接则需要4个步骤。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">第1步，创建一个socket以连接服务器 socket=socket.socket(family,type)</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">第2步，使用socket的connect方法连接服务器 socket.connect((host,port))</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">第3步，客户和服务器通过send和recv方法通信。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">第4步，结束后，客户通过调用socket的close方法来关闭连接。</span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;"><br /></span></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><strong><span style="font-size:14px;">三、一个简单的服务器和客户端通信的例子</span></strong></p><p style="box-sizing: border-box; color: rgb(75, 75, 75); font-family: verdana, Arial, helvetica, sans-seriff; line-height: 20.799999237060547px;"><span style="font-size:14px;">服务器：</span></p>

{% highlight bash %}
import socket
s=socket.socket()
s.bind(('xxx.xxx.xxx.xxx',xxxx))    #ip地址和端口号
s.listen(5)
cs,address = s.accept()
print 'got connected from',address
cs.send('byebye')
ra=cs.recv(512)
print ra
cs.close()
{% endhighlight %}


客户端：

{% highlight bash %}
import socket
s=socket.socket()
s.connect(('xxx.xxx.xxx.xxx',xxxx))   #与服务器程序ip地址和端口号相同
data=s.recv(512)
s.send('hihi')
s.close()
print 'the data received is',data
{% endhighlight %}


运行：

在本机测试（windows环境下，可以将ip地址改为本机ip，端口号在1024以上，windows将1024以下的为保留），运行--CMD--进入命令行模式

先python 服务器程序，后python 客户端程序即可。

或者启动服务器程序后，用telnet ip地址 端口号，也可以得到同样结果。

让server持续接受连接

server.py

{% highlight bash %}
import socket
s=socket.socket()
s.bind(('192.168.43.137',2000))
s.listen(5)

while 1:
    cs,address = s.accept()
    print 'got connected from',address
    cs.send('hello I am server,welcome')
    ra=cs.recv(512)
    print ra
    cs.close()
{% endhighlight %}


测试两个一个程序中两个socket并存是否可行

client.py
{% highlight bash %}
import socket
s=socket.socket()
s.connect(('192.168.43.137',2000))   
data=s.recv(512)
print 'the data received is\n    ',data
s.send('hihi I am client')

sock2 = socket.socket()
sock2.connect(('192.168.43.137',2000))
data2=sock2.recv(512)
print 'the data received from server is\n   ',data2
sock2.send('client send use sock2')
sock2.close()

s.close()
{% endhighlight %}

 
