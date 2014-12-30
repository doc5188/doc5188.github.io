---
layout: post
title: "为Mysql添加远程访问权限"
categories: 数据库
tags: [mysql, mysql远程访问]
date: 2014-12-30 16:10:00
---

下面看看从网上搜集来的几种添加Mysql用户远程访问权限的方法

MySQL上的一个数据库要备份，装了个MySQL的gui工具。打开"MySQL Administrator"工具，填好用户名和密码却登录不了，老是报这个错“ERROR 1130: Host 'lijuan-' is not allowed to connect to this MySQL server”。网上查了下，有这两个方法解决：

解决方法：

* 1。 改表法。可能是你的帐号不允许从远程登陆，只能在localhost。这个时候只要在localhost的那台电脑，登入mysql后，更改 "mysql" 数据库里的 "user" 表里的 "host" 项，从"localhost"改称"%"

<pre>
mysql -u root -pvmwaremysql>use mysql;mysql>update user set host = '%' where user = 'root';mysql>select host, user from user;
</pre>

* 2. 授权法。例如，你想myuser使用mypassword从任何主机连接到mysql服务器的话。

<pre>
GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;
</pre>

如果你想允许用户myuser从ip为192.168.1.3的主机连接到mysql服务器，并使用mypassword作为密码

<pre>
GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'192.168.1.3' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;
</pre>

我的mysql.user里root用户的host果然是localhost，先用改表法给localhost改成“％”，还是不行，仍然报1130的错 误，又按“从任何主机连接到mysql服务器”方法授权，还是报一样的错，最后给自己的ip授权之后，终于登录上了。。。。

乎乎。。。

mysql的ERROR 1045 在上面情况后如再出现客户段1045可在服务器执行如下

<pre>
UPDATE user SET Password=PASSWORD('123456') where USER='myuser';

FLUSH PRIVILEGES;//用户付完权限后对数据进行刷新时用!要不Mysql数据库识别不了
</pre>

例如:(必须参考以上再看下面的例子)

<pre>
GRANT ALL ON *.* TO admin@'%' IDENTIFIED BY 'admin' WITH GRANT OPTION;

mysql "192.168.50.85" "admin" "admin" ;

GRANT ALL ON *.* TO admin@'localhost' IDENTIFIED BY 'admin' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'192.168.50.85' IDENTIFIED BY '123456' WITH GRANT OPTION;

UPDATE user SET Password=PASSWORD('123456') where USER='myuser';

FLUSH PRIVILEGES;
</pre>

mysql默认是没有开启远程控制的，必须添加远程访问的用户。


