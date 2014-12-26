---
layout: post
title: "mysql主从复制（超简单）"
categories: 数据库
tags: [mysql, 主从复制,　mysql集群]
date: 2014-12-26 16:39:16
---

<p style="text-align: center;"><strong><span style="font-size: 22px;">mysql主从复制</span></strong><br>
（超简单）</p>
<p style="text-align: left;">怎么安装mysql数据库，这里不说了，只说它的主从复制，步骤如下：</p>
<p><span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">1、主从服务器分别作以下操作</span></strong><span style="color: rgb(255, 0, 0);">：</span></span><br>
&nbsp; 1.1、版本一致<br>
&nbsp; 1.2、初始化表，并在后台启动mysql<br>
&nbsp; 1.3、修改root的密码<br>
<br>
<strong><span style="font-size: 18px;"><span style="color: rgb(255, 0, 0);">2、修改主服务器master:</span></span></strong><br>
&nbsp;&nbsp; #vi /etc/my.cnf<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [mysqld]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; log-bin=mysql-bin&nbsp;&nbsp; //[必须]启用二进制日志<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; server-id=222&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //[必须]服务器唯一ID，默认是1，一般取IP最后一段<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">3、修改从服务器slave:</span></strong></span><br>
&nbsp;&nbsp; #vi /etc/my.cnf<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [mysqld]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; log-bin=mysql-bin&nbsp;&nbsp; //[必须]启用二进制日志<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; server-id=226&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //[必须]服务器唯一ID，默认是1，一般取IP最后一段<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">4、重启两台服务器的mysql</span></strong></span><br>
&nbsp;&nbsp; /etc/init.d/mysql restart<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">5、在主服务器上建立帐户并授权slave:</span></strong></span><br>
&nbsp;&nbsp; #/usr/local/mysql/bin/mysql -uroot -pmttang&nbsp;&nbsp; <br>
&nbsp;&nbsp; mysql&gt;GRANT REPLICATION SLAVE ON *.* to 'mysync'@'%' identified by 'q123456'; //一般不用root帐号，“%”表示所有客户端都可能连，只要帐号，密码正确，此处可用具体客户端IP代替，如192.168.145.226，加强安全。<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">6、登录主服务器的mysql，查询master的状态</span></strong></span><br>
&nbsp;&nbsp; mysql&gt;show master status;<br>
&nbsp;&nbsp; +------------------+----------+--------------+------------------+<br>
&nbsp;&nbsp; | File&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Position | Binlog_Do_DB | Binlog_Ignore_DB |<br>
&nbsp;&nbsp; +------------------+----------+--------------+------------------+<br>
&nbsp;&nbsp; | mysql-bin.000004 |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 308 |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; +------------------+----------+--------------+------------------+<br>
&nbsp;&nbsp; 1 row in set (0.00 sec)<br>
&nbsp;&nbsp; 注：执行完此步骤后不要再操作主服务器MYSQL，防止主服务器状态值变化<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">7、配置从服务器Slave：</span></strong></span><br>
&nbsp;&nbsp; mysql&gt;change master to aster_host='192.168.145.222',master_user='tb',master_password='q123456',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; master_log_file='mysql-bin.,000004',master_log_pos=308;&nbsp;&nbsp; //注意不要断开，“308”无单引号。<br>
<br>
&nbsp;&nbsp; Mysql&gt;start slave;&nbsp;&nbsp;&nbsp; //启动从服务器复制功能<br>
<br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">8、检查从服务器复制功能状态：</span></strong></span><br>
<br>
&nbsp;&nbsp; mysql&gt; show slave status\G<br>
<br>
&nbsp;&nbsp; *************************** 1. row ***************************<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Slave_IO_State: Waiting for master to send event<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Master_Host: 192.168.2.222&nbsp; //主服务器地址<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Master_User: myrync&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //授权帐户名，尽量避免使用root<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Master_Port: 3306&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //数据库端口，部分版本没有此行<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Connect_Retry: 60<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Master_Log_File: mysql-bin.000004<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Read_Master_Log_Pos: 600&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //#同步读取二进制日志的位置，大于等于&gt;=Exec_Master_Log_Pos<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Relay_Log_File: ddte-relay-bin.000003<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Relay_Log_Pos: 251<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Relay_Master_Log_File: mysql-bin.000004<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Slave_IO_Running: Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //此状态必须YES<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Slave_SQL_Running: Yes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //此状态必须YES<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ......<br>
<br>
注：Slave_IO及Slave_SQL进程必须正常运行，即YES状态，否则都是错误的状态(如：其中一个NO均属错误)。<br>
<br>
以上操作过程，主从服务器配置完成。<br>
&nbsp; <br>
<span style="font-size: 18px;"><strong><span style="color: rgb(255, 0, 0);">9、主从服务器测试：</span></strong></span><br>
<br>
主服务器Mysql，建立数据库，并在这个库中建表插入一条数据：<br>
<br>
&nbsp; mysql&gt; create database hi_db;<br>
&nbsp; Query OK, 1 row affected (0.00 sec)<br>
<br>
&nbsp; mysql&gt; use hi_db;<br>
&nbsp; Database changed<br>
<br>
&nbsp; mysql&gt;&nbsp; create table hi_tb(id int(3),name char(10));<br>
&nbsp; Query OK, 0 rows affected (0.00 sec)<br>
&nbsp;<br>
&nbsp; mysql&gt; insert into hi_tb values(001,'bobu');<br>
&nbsp; Query OK, 1 row affected (0.00 sec)<br>
<br>
&nbsp; mysql&gt; show databases;<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; | Database&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; | information_schema |<br>
&nbsp;&nbsp; | hi_db&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; | mysql&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; | test&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; 4 rows in set (0.00 sec)<br>
<br>
从服务器Mysql查询：<br>
<br>
&nbsp;&nbsp; mysql&gt; show databases;<br>
<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; | Database&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; | information_schema |<br>
&nbsp;&nbsp; | hi_db&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; //I'M here，大家看到了吧<br>
&nbsp;&nbsp; | mysql&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; | test&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |<br>
&nbsp;&nbsp; +--------------------+<br>
&nbsp;&nbsp; 4 rows in set (0.00 sec)<br>
<br>
&nbsp;&nbsp; mysql&gt; use hi_db<br>
&nbsp;&nbsp; Database changed<br>
&nbsp;&nbsp; mysql&gt; select * from hi_tb;&nbsp;&nbsp;&nbsp; //可以看到在主服务器上新增的具体数据<br>
&nbsp;&nbsp; +------+------+<br>
&nbsp;&nbsp; | id&nbsp;&nbsp; | name |<br>
&nbsp;&nbsp; +------+------+<br>
&nbsp;&nbsp; |&nbsp;&nbsp;&nbsp; 1 | bobu |<br>
&nbsp;&nbsp; +------+------+<br>
&nbsp;&nbsp; 1 row in set (0.00 sec)<br>
&nbsp;</p>
<p><strong><span style="font-size: 18px;"><span style="color: rgb(255, 0, 0);">10、完成：</span></span></strong><br>
&nbsp;&nbsp;&nbsp; 编写一shell脚本，用nagios监控slave的两个“yes”，如发现只有一个或零个“yes”，就表明主从有问题了，发短信警报吧。</p>


<pre>
referer:http://369369.blog.51cto.com/319630/790921
</pre>
