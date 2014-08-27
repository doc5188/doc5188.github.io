---
layout: post
title: "freeradius管理程序daloradius"
categories: linux
tags: [linux, freeradius, daloradius]
date: 2014-08-27 15:22:00
---

上一篇说了freeradius的配置，这次介绍一下freeradius的web管理程序daloradius。我们在管理radius服务器的时候，最好的管理就是使用图形界面，都不想使用命令来对用户添加或者是设备添加吧。那好，daloradius就是freeradius最好的图形管理。

废话不多说，下面重点开始介绍配置。

既然上面已经说过是web界面的管理程序，那么首先一点就是先搭建好web环境。

1、web环境搭建

yum groupinstall ‘web server’         //安装web服务程序

yum groupinstall ‘php support’       ///安装php

yum groupinstall ‘mysql database server’    ///这个在配置freeradius时就安装过的

yum install php-mysql        //这个如果不安装，打开php+mysql的程序会出错的

2、下载daloradius

官方下载地址：wget http://nchc.dl.sourceforge.net/project/daloradius/daloradius/daloradius0.9-9/daloradius-0.9-9.tar.gz

3、配置daloradius

将程序解压到/var/www/html目录下面

tar -zxvf daloradius-0.9-9.tar.gz -C /var/www/html/daloradius

修改daloradius目录所有者

Chown –R apache:apache daloradius

4、配置mysql数据库

导入/contrib/db目录下的数据库表

Myslq –u root –p radius < mysql-daloradius.sql

Mysql –u root –p radius < fr2-mysql-daloradius-and-freeradius.sql

修改数据库连接

vim /daloradius/library/daloradius.conf.php

测试

配置好后在浏览器中打开，下面是默认登录用户名和密码

http://yourIP/daloradius

login：administrator

password：radius

问题

1、点击登录页面出错

查看http错误日志信息/var/log/httpd/error_log
<pre>
[Mon Oct 14 15:44:51 2013] [error] [client 172.16.1.55] PHP Warning: include_once(): Failed opening 'DB.php' for inclusion (include_path='.:/usr/share/pear:/usr/share/php') in /var/www/html/daloradius/library/opendb.php on line 84, referer: http://172.16.1.50/daloradius/login.php
[Mon Oct 14 15:44:51 2013] [error] [client 172.16.1.55] PHP Fatal error: Class 'DB' not found in /var/www/html/daloradius/library/opendb.php on line 86, referer: http://172.16.1.50/daloradius/login.php
</pre>

提示数据库连接失败。再次检查连接数据库文件，没有问题。

解决：新版本的daloradius连接数据库，需要安装数据库连接模块。php-pear-DB

没办法安装吧！  yum install php-pear-DB

再次打开web，如果还有出错，安装一下php扩展程序。

下载 ：wget http://pear.php.net/go-pear.phar

安装：php go-gear.phar

OK！一切问题解决完毕。

Daloradius汉化

daloradius汉化包下载：下载地址:http://pan.baidu.com/share/link?shareid=2500086958&uk=3843037427

下载之后，解压然后复制到/daloradius目录下面替换即可，然后登录到web程序里设置语言。

<pre>
引用：http://www.hailiangchen.com/daloradius/
</pre>
