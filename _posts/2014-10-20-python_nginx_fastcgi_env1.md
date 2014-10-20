---
layout: post
title: "nginx上用fastcgi配置python环境(一)"
categories: linux
tags: [fastcgi, python+fastcgi]
date: 2014-10-20 17:33:20
---

费了2天的功夫，翻阅了无数的中文、英文资料，终于搞定。写下此文留待以后翻阅用

本文环境,centOS 5.4 ,Nignx-0.8.49, Python 2.6.5

=====================================================================================
WSGI是Python应用程序或框架和Web服务器之间的一种接口，已经被广泛接受, 它已基本达成它了可移植性方面的目标。  

WSGI 没有官方的实现, 因为WSGI更像一个协议. 只要遵照这些协议,WSGI应用(Application)都可以在任何实现(Server)上运行, 反之亦然。

具体实现有很多种方法，网上有很多的用python写的框架，比如facebook的tornado，我用的是flup，具体的介绍可以到 http://pypi.python.org/pypi/flup/1.0。

{% highlight bash %}
     cd /usr/local/src
     wget http://pypi.python.org/packages/2.5/f/flup/flup-1.0-py2.5.egg#md5=3c9368437e9bffb950c6cce54425d32f
     tar -xzvf flup-1.0.3.dev-20100525.tar.gz
     cd     flup-1.0.3.dev-20100525
     python setup.py install
{% endhighlight %}

到此flup安装完毕

=====================================================================================

以上是准备工作，下面正式开始
  
配置nginx，找到nginx.conf

添加一段如下代码
{% highlight bash %}
 server
  {
    listen  8000;
   server_name test.com;
    location /
    {
       #fastcgi_pass  unix:/tmp/python-cgi.sock;(注1)
      fastcgi_pass  127.0.0.1:8008; (注意这里的端口和上面的listen的8000端口要不一样，否则会报地址已占用的错)
      fastcgi_param SCRIPT_FILENAME "";
      fastcgi_param PATH_INFO $fastcgi_script_name;
      include fcgi.conf;
    }
  }
{% endhighlight %}

注1：这里最好是用127.0.0.1:8000代替，这样的话就没有访问权限的限制，如果用的是python-cgi.sock，还得chmod 777 python-cgi.sock才可以，不然的话浏览器会出现505的内部错误。

 引用原文如下：A Web server can connect to a FastCGI server in one of two ways: It can use either a Unix domain socket (a “named pipe” on Win32 systems), or it can use a TCP socket. What you choose is a manner of preference; a TCP socket is usually easier due to permissions issues.


然后我们再写一个fcgi.py，代码如下
{% highlight bash %}
#!/usr/bin/python
# encoding : utf-8

from flup.server.fcgi import WSGIServer

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!\n']

if __name__  == '__main__':
   WSGIServer(myapp,bindAddress=('127.0.0.1',8008)).run()（注2）
{% endhighlight %}
  
注2，看到了吗，这里的bindAddress 的值是一个元组，这个是WSGIServer的源代码要求这么写的，而且它的值对应的是上面fastcgi-pass的值

然后我们就可以运行python fcgi.py --method=prefork/threaded minspare=50 maxspare=50 maxchildren=1000 (注3)

注3：后面的那些参数相当于php-cgi后面的参数，但是具体的用途还需要进一步探索

运行到这了，我们就可以在浏览器里面敲: http://localhost:8000

如果返回 Hello World,恭喜你，迈出了nginx 运行python的第一步

============================================================================================================


