---
layout: post
title: "Too many connections"
categories: 数据库
tags: [mysql]
date: 2014-12-05 23:43:01
---

Too many connections连接数超过了 MySQL 设置的值，与 max_connections 和 wait_timeout 都有关系。wait_timeout 的值越大，连接的空闲等待就越长，这样就会造成当前连接数越大。


too many connections

错误编号：1040

问题分析：

连接数超过了 mysql教程 设置的值，与 max_connections 和 wait_timeout  都有关系。wait_timeout 的值越大，连接的空闲等待就越长，这样就会造成当前连接数越大。

到c:windows目录下(windows 2000下为winnt)，找到my.ini文件打开后。

在my.ini文件中[mysqld]下添加 

set-variable = max_connections= 10000

然后save modification 保存修改。

最后把mysql重新启动一次即可。
 

解决方法：
<pre>
1、虚拟主机用户请联系空间商优化 mysql 服务器的配置；
2、独立主机用户请联系服务器管理员优化 mysql 服务器的配置，可参考：
修改 mysql 配置文件（windows下为 my.ini， linux下为 my.cnf ）中的参数：
max_connections= 1000
wait_timeout = 5
mysql 5.1以上的修改文件
you can increase this value in main config file (e.g., /etc/my.cnf) using this syntax:
[mysqld]
set-variable=max_connections=250
wait_timeout = 55 代码多长时间自放弃此连接

</pre>
