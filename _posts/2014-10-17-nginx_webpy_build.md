---
layout: post
title: "在Nginx上部署webpy手记"
categories: linux 
tags: [nginx安装webpy]
date: 2014-10-17 16:54:01
---

根据：http://webpy.org/cookbook/fastcgi-nginx :

安装：
<pre>
Nginx-1.0.2
spawn-fcgi
flup
webpy；一种简洁的网络应用框架
</pre>
-
You may replace index.py with your own file name./path/to/www Is the path to the directory where your webpy application is located./path/to/www/index.py is the full path to your 

python file.*Do not run anything until you are at Run*.

<pre>
server {
        listen 80;
        server_name 127.0.0.1:9001
}  

location /static/ {
        root /home/bryan/www; # nginx+webpy application placed here.
        if (-f $request_filename) {
           rewrite ^/static/(.*)$  /static/$1 break;
        }
}
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
        fastcgi_pass 127.0.0.1:9001;
}
</pre>
--

{% highlight bash %}

# cat  /home/bryan/www/index.py
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
{% endhighlight %}
然后别忘记：chmod +x index.py让文件可执行。

--

Start a fastCGI process:
{% highlight bash %}
#!/bin/sh
spawn-fcgi -d /home/bryan/www -f /home/bryan/www/index.py -a 127.0.0.1 -p 9001 #启动一个fastCGI进程
{% endhighlight %}

<pre>
kill 'pgrep -f "python /home/bryan/www/index.py"'
</pre>

--

Run(for reference)

nginx -c /etc/nginx/nginx.conf #no return to shell is OK!

/usr/sbin/nginx reload #reload your new configuration

比如 spawn-fcgi: child exited with: xxx。这时需要检查几点，首先刚才的chmod命令有没有执行，即code.py的可执行属性有没有加上。如果加上以后还不行，那么先把code.py最后加上的web.wsgi.runwsgi = lambda func…这句代码加#号注释掉，然后执行python code.py看是否出现刚才说的http://0.0.0.0:8080，如果代码报错，如[Errno 98] Address already in use，说明刚才python可能没有正常结束，还占用着这个地址，直接killall python，或者用 ps aux | grep “python” 查出python对应的PID，通过kill PID来结束。

--

*打开nginx服务器*

在成功开启一个spawn-fcgi进程后，我们就可以打开nginx了：

nginx -t -c /etc/nginx/nginx.conf #测试配置文件是否正确；

nginx -c /etc/nginx/nginx.conf #打开Nginx服务器

现在可以从你的浏览器测试：Hello,World!

还有：

/etc/init.d/nginx start启动Nginx

service nginx restart/stop等都可以用。

man nginx查看nginx手册页。

--

在AWS上部署，根据这里指引（我都自己测试通过的）。

祝大家好运！

