---
layout: post
title: "Linux查看端口占用情况,并强制释放占用的端口" 
categories: linux
tags: [linux]
date: 2015-01-26 15:16:13
---

有时候关闭软件后，后台进程死掉，导致端口被占用。下面以TOMCAT端口8060被占用为例，列出详细解决过程。

解决方法：

1.查找被占用的端口

<pre>
    netstat -tln  
    netstat -tln | grep 8060
</pre>

 netstat -tln 查看端口使用情况，而netstat -tln | grep 8060则是只查看端口8060的使用情况

 

2.查看端口属于哪个程序？端口被哪个进程占用

{% highlight bash %}
lsof -i:8060

 COMMAND   PID   USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME

java    20804   root   36u  IPv6 35452317      0t0  TCP *:pcsync-https (LISTEN)
{% endhighlight %}

3.杀掉占用端口的进程  根据pid杀掉

kill -9 进程id 

kill -9 20804


---------------------------------------------------------------------------------------------------------

在Linux操作系统中

查看占用某一端口的进程是什么:#lsof -i:端口号

{% highlight bash %}
[root@oa test]# lsof -i:21

COMMAND PID USER FD TYPE DEVICE SIZE NODE NAME

vsftpd 2616 root 3u IPv4 7519 TCP *:ftp (LISTEN)
{% endhighlight %}


<pre>
referer:http://blog.itpub.net/27058265/viewspace-732970/
</pre>
