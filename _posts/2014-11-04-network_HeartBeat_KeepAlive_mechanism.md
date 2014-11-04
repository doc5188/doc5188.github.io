---
layout: post
title: "闲说HeartBeat心跳包和TCP协议的KeepAlive机制"
categories: 网络
tags: [heartbeat, keepalive]
date: 2014-11-04 12:26:41
---

这篇文章还是写得蛮容易理解的

很多应用层协议都有HeartBeat机制，通常是客户端每隔一小段时间向服务器发送一个数据包，通知服务器自己仍然在线，并传输一些可能必要的数据。使用心跳包的典型协议是IM，比如QQ/MSN/飞信等协议。

学过TCP/IP的同学应该都知道，传输层的两个主要协议是UDP和TCP，其中UDP是无连接的、面向packet的，而TCP协议是有连接、面向流的协议。

所以非常容易理解，使用UDP协议的客户端（例如早期的“OICQ”，听说OICQ.com这两天被抢注了来着，好古老的回忆）需要定时向服务器发送心跳包，告诉服务器自己在线。

然而，MSN和现在的QQ往往使用的是TCP连接了，尽管TCP/IP底层提供了可选的KeepAlive（ACK-ACK包）机制，但是它们也还是实现了更高层的心跳包。似乎既浪费流量又浪费CPU，有点莫名其妙。

具体查了下，TCP的KeepAlive机制是这样的，首先它貌似默认是不打开的，要用setsockopt将SOL_SOCKET.SO_KEEPALIVE设置为1才是打开，并且可以设置三个参数tcp_keepalive_time/tcp_keepalive_probes/tcp_keepalive_intvl，分别表示连接闲置多久开始发keepalive的ack包、发几个ack包不回复才当对方死了、两个ack包之间间隔多长，在我测试的Ubuntu Server 10.04下面默认值是7200秒（2个小时，要不要这么蛋疼啊！）、9次、75秒。于是连接就了有一个超时时间窗口，如果连接之间没有通信，这个时间窗口会逐渐减小，当它减小到零的时候，TCP协议会向对方发一个带有ACK标志的空数据包（KeepAlive探针），对方在收到ACK包以后，如果连接一切正常，应该回复一个ACK；如果连接出现错误了（例如对方重启了，连接状态丢失），则应当回复一个RST；如果对方没有回复，服务器每隔intvl的时间再发ACK，如果连续probes个包都被无视了，说明连接被断开了。

这里有一篇非常详细的介绍文章： http://tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO ，包括了KeepAlive的介绍、相关内核参数、C编程接口、如何为现有应用（可以或者不可以修改源码的）启用KeepAlive机制，很值得详读。

这篇文章的2.4节说的是“Preventing disconnection due to network inactivity”，阻止因网络连接不活跃（长时间没有数据包）而导致的连接中断，说的是，很多网络设备，尤其是NAT路由器，由于其硬件的限制（例如内存、CPU处理能力），无法保持其上的所有连接，因此在必要的时候，会在连接池中选择一些不活跃的连接踢掉。典型做法是LRU，把最久没有数据的连接给T掉。通过使用TCP的KeepAlive机制（修改那个time参数），可以让连接每隔一小段时间就产生一些ack包，以降低被T掉的风险，当然，这样的代价是额外的网络和CPU负担。

前面说到，许多IM协议实现了自己的心跳机制，而不是直接依赖于底层的机制，不知道真正的原因是什么。

就我看来，一些简单的协议，直接使用底层机制就可以了，对上层完全透明，降低了开发难度，不用管理连接对应的状态。而那些自己实现心跳机制的协议，应该是期望通过发送心跳包的同时来传输一些数据，这样服务端可以获知更多的状态。例如某些客户端很喜欢收集用户的信息……反正是要发个包，不如再塞点数据，否则包头又浪费了……

大概就是这样吧，如果有大牛知道真正的原因，还望不吝赐教。


@2012-04-21 

p.s. 通过咨询某个做过IM的同事，参考答案应该是，自己实现的心跳机制通用，可以无视底层的UDP或TCP协议。如果只是用TCP协议的话，那么直接使用KeepAlive机制就足够了。


查看：

</pre>
# cat /proc/sys/net/ipv4/tcp_keepalive_time
  7200 

# cat /proc/sys/net/ipv4/tcp_keepalive_intvl
  75 

# cat /proc/sys/net/ipv4/tcp_keepalive_probes
  9
</pre>

修改：

<pre>
# echo 600 > /proc/sys/net/ipv4/tcp_keepalive_time 

# echo 60 > /proc/sys/net/ipv4/tcp_keepalive_intvl 

# echo 20 > /proc/sys/net/ipv4/tcp_keepalive_probes
</pre>



我想这里只是设置每个socket的默认值，具体在创建socket的时候，可以对每个socket进行设置。



<pre>
referer:
http://blog.sina.com.cn/s/blog_7a3510120101775w.html
</pre>
