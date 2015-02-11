---
layout: post
title: "MySQL 5.6.14 win32 zip版安装"
categories: 数据库
tags: [mysql安装]
date: 2015-02-11 00:42:12
---

<p>1 从<a target="_blank" target="_blank" href="http://dev.mysql.com/downloads/mysql/">http://dev.mysql.com/downloads/mysql/</a>&nbsp; 下载MySQL Community Server的Windows 平台mysql-5.6.14-win32.zip压缩包</p>

<p>2 将文件解压至F:\mysql-5.6.14-win32</p>

<p>3 切换至目录F:\mysql-5.6.14-win32，将文件my-default.ini复制一份重命名为my.ini放到当前目录下</p>

<p>4 打开my.ini进行MySQL配置，主要设置以下几项：</p>

<p></p>

<pre code_snippet_id="99111" snippet_file_name="blog_20131205_1_6953867"  code_snippet_id="99111" snippet_file_name="blog_20131205_1_6953867" name="code" class="plain">[mysqld]
#这一句解决有IPV6协议的计算机上默认采用IPV6协议导致无法从程序连接数据库的问题
bind-address = 127.0.0.1
#设置MySQL Server的字符集
character-set-server=utf8

[client]
#设置MySQL客户端的字符集
default-character-set=utf8
</pre>5 将MySQL的F:\mysql-5.6.14-win32\bin目录加入系统环境变量

<p></p>

<p>6 在CMD控制台将目录切换到F:\mysql-5.6.14-win32\bin，运行： mysqld -install 安装MySQL的服务，然后到服务列表中启动它</p>

<p>7 在CMD控制台下运行mysqladmin -uroot -p password 123456并回车，设置root用户新密码为123456。接下来输入密码的提示是指输入原密码，初始root密码为空</p>

<p>8 在CMD控制台下运行mysql -uroot -p，根据提示输入密码成功后就可以使用MySQL了</p>


<pre>
referer:http://blog.csdn.net/fengbingyang/article/details/17149769
</pre>
