---
layout: post
title: "RHEL6 配置shellinabox远程Terminal模拟器"
categories: linux
tags: [linux, shellinabox, web terminal]
date: 2014-09-30 12:35:23
---

   Shellinabox 是一个利用 Ajax 技术构建的基于 Web 的远程 Terminal 模拟器，也就是说安装了该软件之后，不需要开启 ssh服务，通过 Web 网页就可以对远程主机进行维护操作了，出于安全考虑， Shellinabox 默认强制使用了https协议,这是个挺有趣的技术，因而就在rhel6上面折腾了下，下面记录了主要的操作步骤

一：编译安装Shellinabox
{% highlight bash %}
[root@rhel6 ~]# cd /usr/local/src/tarbag/
[root@rhel6 tarbag]# wget http://shellinabox.googlecode.com/files/shellinabox-2.10.tar.gz
[root@rhel6 tarbag]# tar -zxvf shellinabox-2.10.tar.gz -C ../software/
[root@rhel6 tarbag]# cd ../software/shellinabox-2.10/
[root@rhel6 shellinabox-2.10]# ./configure --prefix=/usr/local/shellinabox
[root@rhel6 shellinabox-2.10]# make && make install
{% endhighlight %}

二：试启动Shellinabox，可以加上--help参数查看启动选项，这里可以看到默认Shellinabox采用https方式启动
{% highlight bash %}
[root@rhel6 ~]# /usr/local/shellinabox/bin/shellinaboxd
Cannot read valid certificate from "certificate.pem". Check file permissions and file format.

[root@rhel6 ~]# /usr/local/shellinabox/bin/shellinaboxd -b -t  //-b选项代表在后台启动，-t选项表示不使用https方式启动，默认以nobody用户身份，监听TCP4200端口

[root@rhel6 ~]# netstat -ntpl |grep shell
tcp        0      0 0.0.0.0:4200                0.0.0.0:*                   LISTEN      16823/shellinaboxd 

[root@rhel6 ~]# killall  shellinaboxd
{% endhighlight %}


三：生成pem证书，以https方式启动，pem证书的格式为公钥加私钥，并以x509的格式进行打包
{% highlight bash %}
[root@rhel6 ~]# openssl genrsa -des3 -out my.key 1024  
[root@rhel6 ~]# openssl req -new -key my.key  -out my.csr
[root@rhel6 ~]# cp my.key my.key.org
[root@rhel6 ~]# openssl rsa -in my.key.org -out my.key
[root@rhel6 ~]# openssl x509 -req -days 3650 -in my.csr -signkey my.key -out my.crt
[root@rhel6 ~]# cat my.crt my.key > certificate.pem

[root@rhel6 ~]# /usr/local/shellinabox/bin/shellinaboxd -c /root -u root -b  //-c参数指定pem证书目录，默认证书名为certificate.pem，-u 选项指定启动的用户身份
[root@rhel6 ~]# netstat -ntpl |grep 4200
tcp        0      0 0.0.0.0:4200                0.0.0.0:*                   LISTEN      26445/shellinaboxd 

[root@rhel6 ~]# ps -ef |grep shell
root     26445     1  0 14:03 ?        00:00:00 /usr/local/shellinabox/bin/shellinaboxd -c /root -u root -b
root     26446 26445  0 14:03 ?        00:00:00 /usr/local/shellinabox/bin/shellinaboxd -c /root -u root -b
{% endhighlight %}
 
<img src="/upload/images/142336482.jpg" />

<img src="/upload/images/142401533.jpg" />
 

 
<pre>
本文出自 “斩月” 博客，请务必保留此出处http://ylw6006.blog.51cto.com/470441/463630
</pre>
