---
layout: post
title: "TCP连接与防火墙"
categories: 网络 
tags: [TCP连接与防火墙]
date: 2014-11-04 12:47:47
---

TCP连接与防火墙

通常，我们的Tcp服务器会放在IDC机房的某一个或几个防火墙后面，客户端与服务器之间的TCP连接会经过防火墙中转，如下图所示：

<img src="upload/images/TcpFirewall.JPG" />
    
在这种情况下，有一点特别需要注意：当Firewall与Server之间的Tcp连接在一段时间（如10分钟）内没有任何应用层的消息经过时，Firewall可能会主动断开与Server之间的Tcp连接，但是Client与Firewall之间的连接一直是有效的。这种情况下，Server以为Client已经断开连接了，而Client却以为自己和Server之间的连接还保持着。

我们在进行公网测试的时候发现了这个问题，而这样的问题在内网中是无法重现的。
