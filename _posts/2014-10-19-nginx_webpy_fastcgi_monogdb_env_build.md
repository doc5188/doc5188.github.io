---
layout: post
title: "nginx+web.py+spawn-fcgi+mongodb搭建"
categories: linux
tags: [nginx, webpy,spawn-fcgi, mongodb]
date: 2014-10-19 22:27:34
---

* 1、安装python 2.7.3

注意，在还没有安装之前先使用python -V查看下版本，一般情况下都会安装低版本

如果已经有安装低版本的，请使用

{% highlight bash %}
# mv /usr/bin/python /usr/bin/python24
{% endhighlight %}

这样修改后，如果之前的脚本使用的是旧版本的话，请修改将/#!/usr/bin/python改为#!/usr/bin/python24即可
{% highlight bash %}
# wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
# tar zxvf Python-2.7.3.tar.bz2
# cd Python-2.7.3
{% endhighlight %}
注意：如果想要支持其他模块，请修改./Modules/Setup.dist这个文件，把需要添加模块的前面的#号注释去掉

{% highlight bash %}
# ./configure --prefix=/usr/local/python27 --enable-unicode=ucs4
# make
# make install
# ln -s /usr/local/python27/bin/python /usr/bin/python
# ln -s /usr/local/python27/bin/python2.7 /usr/bin/python2.7到这里新版本python2.7.3安装完成
{% endhighlight %}
python -V 查看

* 2、安装easy_install,方便安装第三方扩展包

{% highlight bash %}
# wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg
{% endhighlight %}
下载后安装
{% highlight bash %}
sh setuptools-0.6c11-py2.7.egg
{% endhighlight %}

会自动安装后，安装在/usr/local/python27/bin/这个目录，做个软链接，方便使用
{% highlight bash %}
# ln -s /usr/local/python27/bin/easy_install* /usr/bin/
{% endhighlight %}

* 3、安装web.py使用easy_install命令

easy_install web.py测试安装是否正常

{% highlight bash %}
[root@localhost Python-2.7.3]# python
Python 2.7.3 (default, Aug 31 2012, 18:37:11)
[GCC 4.1.2 20080704 (Red Hat 4.1.2-44)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import web
>>>

{% endhighlight %}

##########如果出现以上这个情况，说明已经安装好web.py#################

* 4、安装Spawn-fcgi

在安装安装Spawn-fcgi之前要安装flup

{% highlight bash %}
# easy_install flup
# wget http://www.lighttpd.net/download/spawn-fcgi-1.6.3.tar.bz2
# tar xvf spawn-fcgi-1.6.3.tar.bz2
# cd spawn-fcgi-1.6.3
# ./configure --prefix=/usr/local/spawn-fcgi
# make
# make install
# 
# #做个软链接
# ln -s /usr/local/spawn-fcgi/bin/spawn-fcgi /usr/bin/
{% endhighlight %}

* 5、安装pcre-8.20.tar.bz2

在安装之前，说一个小小的问题,pcre-8.30.tar.bz2与nginx-1.2.3.tar.gz有不兼容的问题

{% highlight bash %}
# tar zxvf pcre-8.20.tar.bz2
# cd pcre-8.30
# ./configure
# make
# make install
{% endhighlight %}

* 6、安装nginx

{% highlight bash %}
# yum -y pcre-devel openssl-devel install zlib-devel
# wget http://nginx.org/download/nginx-1.2.3.tar.gz
# tar zxvf nginx-1.2.3.tar.gz
# cd nginx-1.2.3
# ./configure --prefix=/usr/local/nginx --with-pcre --with-http_stub_status_module --with-openssl=/usr/
# make
# make install
{% endhighlight %}


* 7、配置nginx.conf
<pre>
user  nobody;
worker_processes  4;
pid        logs/nginx.pid;

events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    gzip  on;
    server {
        listen       80;
        server_name  localhost;

        location / {
            include fastcgi_params;
             fastcgi_param SCRIPT_FILENAME $fastcgi_script_name;
             fastcgi_param PATH_INFO $fastcgi_script_name;
             fastcgi_pass unix:/tmp/pyweb.sock;
             fastcgi_param SERVER_ADDR $server_addr;
             fastcgi_param SERVER_PORT $server_port;
             fastcgi_param SERVER_NAME $server_name;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
  }
}
</pre>
#################################配置nginx.conf完成#####################################
 
* 8、测试
<pre>
vi /usr/local/nginx/html/index.py
#!/usr/bin/env python
#-*-coding:utf8-*-
import web
urls = ("/.*", "hello")
app = web.application(urls, globals())
class hello:
        def GET(self):
                 return 'hello python and web.py'
if __name__ == "__main__":
         web.wsgi.runwsgi = lambda func, addr = None: web.wsgi.runfcgi(func, addr)
         app.run()
</pre>

退出，chmod +x /usr/local/nginx/html/index.py给予权限，这个就是入口文件

启动spawn-fcgi,并创建进程

spawn-fcgi -d /usr/local/nginx/html/ -f /usr/local/nginx/html/index.py  -s /tmp/pyweb.sock -u nobody -g nobody   (这里的用户最好是与nginx用户一致)

浏览器访问效果（如图:
 

 
<img src="/upload/images/1A00VE9-0.jpg" /> 
 

* 9、安装python的mongodb的驱动，也就是pymongo模块

easy_install pymongo

测试模块
{% highlight bash %}
[root@localhost html]# python
Python 2.7.3 (default, Aug 31 2012, 18:37:11)
[GCC 4.1.2 20080704 (Red Hat 4.1.2-44)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import pymongo
>>>
{% endhighlight %}
#######################说明正常######################################
 
 
 
* 10、安装mongodb数据库
<pre>

/usr/sbin/groupadd -g 690 mongodb
/usr/sbin/useradd -g mongodb mongodb -u 690 -s /sbin/nologin
wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.0.0.tgz(我的系统是64位)
tar zxvf mongodb-linux-x86_64-2.0.0.tgz
mv mongodb-linux-x86_64-2.0.0 /usr/local/
ln -s /usr/local/mongodb/bin/*  /bin/
mkdir -p /data/db/
chown -R mongodb.mongodb /data/db/
</pre> 
 
 
 
* 11、启动:mongdb
<pre>
nohup mongod --dbpath /data/db &
mongod --fork --port 25000 --auth --dbpath /data/db/ --logpath /data/mongodb.log(日志文件最好与数据文件放同一个地方,默认端口27017,这里使用25000)
</pre>
 
 
 
* 12、查看端口
{% highlight bash %}
[root@localhost data]# netstat -ln|grep -E "25000|26000"
tcp        0      0 0.0.0.0:25000               0.0.0.0:*                   LISTEN     
tcp        0      0 0.0.0.0:26000               0.0.0.0:*                   LISTEN     
unix  2      [ ACC ]     STREAM     LISTENING     288568 /tmp/mongodb-25000.sock
{% endhighlight %}
 
 
 
* 13、登陆测试
<pre>
[root@localhost data]# mongo --host 192.168.250.109:25000
MongoDB shell version: 2.2.0
connecting to: 192.168.250.109:25000/test
>
</pre>
 

web管理:http://IP:26000

解释下参数
<pre>
dbpath: 数据文件存放路径，每个数据库会在其中创建一个子目录。
logpath：错误日志文件
fork： 以后台Daemon形式运行服务
port： 对外服务端口默认端口27017。
</pre>

Web管理端口在这个port的基础上+1000，这里可以使用http://IP:26000管理

本文出自 “游造技术博客” 博客，请务必保留此出处http://youzao.blog.51cto.com/3946111/987292
