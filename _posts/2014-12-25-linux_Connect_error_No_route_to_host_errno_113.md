---
layout: post
title: "Connect error: No route to host(errno:113) 连接错误解决办法－－关闭iptables防火墙 "
categories: linux
tags: [linux, iptables防火墙, socket]
date: 2014-12-25 12:16:07
---

两台机器进行socket通信时，可能在连接时出现错误：

connect error: No route to host(errno:113)

出错原因：server端的防火墙设置了过滤规则

解决办法：使用iptables关闭server端的防火墙

1.暂时关闭

<pre>
$ sudo service iptables stop
</pre>

2.打开

<pre>
$ sudo service iptables start
</pre>

3.永久打开和关闭

<pre>
$ sudo chkconfig iptables on

$ sudo chkconfig iptables off
</pre>


<pre>
referer:http://blog.csdn.net/miaohongyu1/article/details/11472469
</pre>
