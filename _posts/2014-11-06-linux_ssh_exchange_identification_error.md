---
layout: post
title: "ssh问题：ssh_exchange_identification: Connection closed by remote host..."
categories: linux
tags: [ssh_exchange_identification]
date: 2014-11-06 09:22:09
---


ssh问题：ssh_exchange_identification: Connection closed by remote host...

刚刚一个朋友告诉我SSH连接不上服务器了,重启电脑也不管用.我仔细看了一下,老报如下错误:

ssh_exchange_identification: Connection closed by remote host

the connection to the remote host was lost . this usually means that you network connection went down or that the remote host was rebooted
most network outages are short. and thus trying again may work

我在网上google了一下,得解决方案:

(1)  最简单的解决方法就是让/etc/hosts.allow 和/etc/hosts.deny里面的所有信息都不生效,全部注销掉,重启SSH服务就可以了.

但是，有时候在你修改后不久，仍然会出现/etc/hosts.deny自动修改，让你还是登录不了，此时需要检查denyhosts服务。

 在redhat系列的版本中，有一个denyhosts服务，会自动覆盖/etc/hosts.deny文件，在确认要登录的机器没有问题时，可以简单做如下处理：

/etc/init.d/denyhosts stop

(2)  但是还有一种情况，就是客户端连接数过多时，也会报这个错误。缺省情况下，SSH终端连接数最大为10个。在这种情况下，需要改SSH的配置文件，

解决方案：

<pre>
1)        修改/etc/ssh/sshd_config中#MaxStartups 10，将其改为MaxStartups 1000
2)        重启SSH服务，/etc/init.d/ssh restart
</pre>

