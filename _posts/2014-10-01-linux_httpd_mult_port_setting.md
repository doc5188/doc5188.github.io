---
layout: post
title: "配置httpd监听多个http端口"
categories: linux
tags: [linux, httpd]
date: 2014-10-01 11:20:01
---

默认的，红帽企业版Linux 5上的httpd监听http 80端口。 有些时候，httpd还需要监听除了80之外的端口。在配置文件/etc /httpd/conf/httpd.conf里，Listen选项告诉httpd响应指定端口的请求。有时候使用多个Listen选项来指定httpd 多个监听的端口。

修改配置文件/etc/httpd/conf/httpd.conf，将


Listen 80

 

改为

Listen 80
Listen 81
Listen 82

这里端口80, 81 和 82 是httpd要监听的端口。重启httpd服务：

{% highlight bash %}
# service httpd restart
{% endhighlight %}

 

使用命令netstat来检查修改后的情况：

{% highlight bash %}
# netstat -anp | grep httpd
tcp        0      0 :::80                       :::*        LISTEN      5278/httpd          
tcp        0      0 :::81                       :::*        LISTEN      5278/httpd         
tcp        0      0 :::82                       :::*        LISTEN      5278/httpd        
<snip>
{% endhighlight %}

 

现在， httpd监听端口80， 81和82。
