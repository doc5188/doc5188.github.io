---
layout: post
title: "linux下使用webpy搭建python的web开发"
categories: python
tags: [python, webpy]
date: 2014-10-02 21:38:32
---

基于python的web开发，这里我们使用linux为开发环境，搭建基于nginx + web.py + fastcgi

有些基本基本概念解释下，哈哈，因为我不懂
<pre>
1.wsgi为Web服务器网关接口(Python Web Server Gateway Interface，缩写为WSGI)是是为Python语言定义的Web服务器和Web应用程序或框架之间的一种简单而通用的接口。自从WSGI被开发出来以后，许多其它语言中也出现了类似接口
2.uwsgi，另一种python定义的web服务器和web应用的接口
3.REST服务,REST(Representational State Transfer表述性状态转移)是一种针对网络应用的设计和开发方式，可以降低开发的复杂性，提高系统的可伸缩性。
4.CRUD是指在做计算处理时的增加(Create)、查询(Retrieve)（重新得到数据）、更新(Update)和删除(Delete)几个单词的首字母简写。主要被用在描述软件系统中数据库或者持久层的基本操作功能
</pre>

以下内容主要来自

http://webpy.org/cookbook/fastcgi-nginx

需要的软件
<pre>
nginx 0.7以上版本,我使用的是nginx 0.9.2
webpy我使用的web.py-0.37 (http://webpy.org/)
spawn-fcgi 1.6.3(http://redmine.lighttpd.net/projects/spawn-fcgi/news)
flup 1.0(http://trac.saddi.com/flup)
</pre>

nginx的配置请参看官方文档

spawn-fcgi是lighttpd的一个子项目用于多进程管理

webpy和flup安装方式为解压后运行python setup.py install

安装编写index.py

<pre>
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import web

    urls = ("/.*", "hello")
    app = web.application(urls, globals())

    class hello:
        def GET(self):
            return 'Hello, world!'

    if __name__ == "__main__":
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
        app.run()
</pre>

注意index.py需要使用命令chmod +x index.py加入可执行权限

将index.py放入/data/www(我所使用的目录你可以修改)

修改nginx.conf配置

index要加入index.py

Nginx的配置加入

点击(此处)折叠或打开

<pre>
    location / {
            fastcgi_param REQUEST_METHOD $request_method;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_param CONTENT_TYPE $content_type;
            fastcgi_param CONTENT_LENGTH $content_length;
            fastcgi_param GATEWAY_INTERFACE CGI/1.1;
            fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;
            fastcgi_param REMOTE_ADDR $remote_addr;
            fastcgi_param REMOTE_PORT $remote_port;
            fastcgi_param SERVER_ADDR $server_addr;
            fastcgi_param SERVER_PORT $server_port;
            fastcgi_param SERVER_NAME $server_name;
            fastcgi_param SERVER_PROTOCOL $server_protocol;
            fastcgi_param SCRIPT_FILENAME $fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_script_name;
            fastcgi_pass 127.0.0.1:9002;
    }
</pre>

使用Spawn-fcgi

spawn-fcgi -d /data/www -f /data/www/index.py -a 127.0.0.1 -p 9002

如果报错为126，说明index.py没有可执行权限

netstat -lnp | grep 9002参考是否启动成功

我运行的实际为

spawn-fcgi -d /data/www -f /data/www/index.py -a 127.0.0.1 -p 9002 -F 2

启动2个进程

启动nginx

浏览器输入地址

成功结束

参考的文章如下
<pre>
http://www.vimer.cn/2011/07/linux%E4%B8%8Bnginxpythonfastcgi%E9%83%A8%E7%BD%B2%E6%80%BB%E7%BB%93web-py%E7%89%88.html
http://timyang.net/python/python-webpy-lighttpd/
http://timyang.net/python/python-rest/ 
</pre>
