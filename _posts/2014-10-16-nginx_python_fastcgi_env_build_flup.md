---
layout: post
title: "nginx+python+fastcgi环境配置(flup版本)"
categories: linux
tags: [nginx+python+fastcgi]
date: 2014-10-16 23:37:20
---

 昨天花了一整天的时间研究搭建了nginx+python+fastcgi环境，并测试没问题，由于是第一次，并且参考了网上很多东西，网上也有很多，但还是把自己的过程记录下。

主要感谢这位兄弟的文章给了我很大的帮忙http://blog.csdn.net/linvo/article/details/5870498，不过这位兄弟的测试代码我没跑成功。

* 一、环境配置主要分以下几步：

* 1、Linux环境和python环境(此步骤省略)

* 2、Nginx环境、flup、spawn-fcgi工具的部署如下


{% highlight bash %}
# wget http://nginx.org/download/nginx-1.2.1.tar.gz  
# tar -xzvf nginx-1.2.1.tar.gz  
# cd nginx-1.2.1  
# ./configure --prefix=/usr/local/nginx-1.2.1 --with-http_stub_status_module --with-http_ssl_module --with-cc-opt='-O2'  
# make  
# make install  
#   
# wget http://www.saddi.com/software/flup/dist/flup-1.0.2.tar.gz  
# tar -xzvf flup-1.0.2.tar.gz  
# cd flup-1.0.2  
# python setup.py install  
#   
# http://www.lighttpd.net/download/spawn-fcgi-1.6.3.tar.gz  
# tar -xzvf spawn-fcgi-1.6.3.tar.gz  
# cd spawn-fcgi-1.6.3  
# ./configure  
# make  
# make install  

{% endhighlight %}

默认位置在/usr/local/bin/spawn-fcgi  

* 二、配置nginx.conf支持fastcgi

具体配置不详说，下面是配置的一个虚拟主机。/naiveloafer.cgi就是配置的fastcgi，请求会转发到5678端口的程序，配置好后重启nginx服务。


<pre>
server {  
        listen      83;  
        server_name naiveloafer.xxx.com;  
        access_log  logs/naiveloafer.xxx.com main;  
        location / {  
            root /usr/local/nlweb/htdocs;  
            index index.html index.htm;  
        }  
        location /naiveloafer.cgi {  
            fastcgi_pass 127.0.0.1:5678;  
            include fastcgi.conf;  
        }  
    }  
</pre>


编写fcgi脚本，并保存为fcgi.py：

<pre>
#!/usr/bin/env python  
#coding=utf-8  
#author:naiveloafer  
#date:2012-06-07  
  
from flup.server.fcgi import WSGIServer  
  
def naiveloafer_app(environ, start_response):  
    start_response('200 OK', [('Content-Type', 'text/plain')])  
    content = "Hello World!naiveloafer"  
    return [content]  
  
if __name__  == '__main__':  
   WSGIServer(naiveloafer_app).run()  
</pre>


开启监听，具体参数见那位兄弟的文章

{% highlight bash %}
# spawn-fcgi -f /usr/local/nlweb/cgi-bin/fcgi.py -a 127.0.0.1 -p 5678 -u nobody -F 5  
{% endhighlight %}


至此，通过web或者HTTP请求就能从fastcgi返回信息了。但这只是一个具体的配置

具体如何处理请求的参数，获取请求的数据看

<pre>
出处:http://blog.csdn.net/naiveloafer/article/details/7640853
</pre>
