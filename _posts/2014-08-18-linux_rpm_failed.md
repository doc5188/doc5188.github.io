---
layout: post
title: "linux安装mysql提示conflicts with file from package的解决方法"
categories: linux
tags: [linux, rpm, mysql]
date: 2014-08-18 15:13:21
---
linux安装mysql提示conflicts with file from package的解决办法！

在linux下面安装 mysql的时候出现了错误：
{% highlight bash %}
[root@localhost local]# rpm -ivh MySQL-server-5.5.24-1.el6.i686.rpm 

Preparing...                ########################################### [100%]
        file /usr/share/mysql/charsets/cp1251.xml from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/czech/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/danish/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/dutch/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/english/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/estonian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/french/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/german/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/greek/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/hungarian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/italian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/japanese/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/korean/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/norwegian-ny/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/norwegian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/polish/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/portuguese/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/romanian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/russian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/serbian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/slovak/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/spanish/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/swedish/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
        file /usr/share/mysql/ukrainian/errmsg.sys from install of MySQL-server-5.5.24-1.el6.i686 conflicts with file from package mysql-libs-5.1.52-1.el6_0.1.i686
{% endhighlight %}

 

原因由包冲突引起的！

解决思路，先移除冲突的libs包，在进行安装 

 

yum -y remove mysql-libs-5.1.52*        

-y的意思就是不用询问是否remove

卸载完成之后，再安装MySQL成功了

rpm -ivh MySQL-server-5.5.24-1.el6.i686.rpm 
