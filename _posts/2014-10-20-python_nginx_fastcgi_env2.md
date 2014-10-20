---
layout: post
title: "nginx上用fastcgi配置python环境(二)"
categories: linux
tags: [fastcgi, python+fastcgi]
date: 2014-10-20 17:36:20
---
前几天写了   nginx上用fastcgi配置python环境(一)，在那篇文章里面我用的是最简单的配置，在这篇文章里面我将进一步介绍

需要的软件 : 
<pre>
Linux ,
nginx ,
spawn-fcgi(一个fastcgi的管理工具) ,
flup（用python写的实现WSGI的模块，这个很重要，详细介绍http://pypi.python.org/pypi/flup/1.0）,
</pre>
                    
===============================================================================================

下载安装好上面说的软件。nginx配置这些和上一篇文章的一样，就不说了
<pre>
说说spawn-fcgi ： spawn-fcgi  -f /data/www/python/fcgi.py -a 127.0.0.1 -p 8008  -F 5 -P /var/run/fcgi.pid -u www
                      
                   -f 要执行的文件（不理解的可以思考php-cgi这个命令）
                   -a 监听的地址
                   -p 监听的端口(这个不是nginx监听的网络端口，而是nginx的fastcgi-pass传过来的端口)
                   -F fastcgi开启的进程数(不理解的可以思考下php的php-cgi数目)
                   -P 开启的进程的进程号所写入的文件（有了这个就可以很轻松的杀掉开启的fasgcgi）
                   -u  以什么用户身份运行（这里有root会报错，不知道什么原因）
</pre>


===============================================================================================
下面上代码，代码很简单

{% highlight bash%}
#!/usr/bin/python

import flup.server.fcgi as flups

def myapp(environ, start_response):   
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ["how do you do\n"]
    
if __name__  == '__main__':
    #WSGIServer(myapp,bindAddress=('127.0.0.1',8008)).run()（如果是直接用flup而不用fastcgi就用它）
    flups.WSGIServer(myapp).run() （如果是fastcgi的话就用它）
{% endhighlight %}


在浏览器输入 http://localhost:8000

如果返回 how do you do ,恭喜你，迈出了nginx 运行python的第二步
