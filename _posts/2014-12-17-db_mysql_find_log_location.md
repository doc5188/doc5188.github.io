---
layout: post
title: "mysql日志文件在哪"
categories: 数据库
tags: [mysql, mysql日志]
date: 2014-12-17 09:46:09
---

登录mysql终端

日志文件路径
<pre>
mysql> show variables like 'general_log_file';
+------------------+------------------------------------+
| Variable_name    | Value                              |
+------------------+------------------------------------+
| general_log_file | /usr/local/mysql/data/localhost.log |
+------------------+------------------------------------+
1 row in set (0.00 sec)
</pre>

错误日志文件路径

<pre>
mysql> show variables like 'log_error';
+---------------+------------------------------------+
| Variable_name | Value                              |
+---------------+------------------------------------+
| log_error     | /usr/local/mysql/data/localhost.err |
+---------------+------------------------------------+
1 row in set (0.00 sec)
</pre>

慢查询日志文件路径

<pre>
mysql> show variables like 'slow_query_log_file';
+---------------------+-----------------------------------------+
| Variable_name       | Value                                   |
+---------------------+-----------------------------------------+
| slow_query_log_file | /usr/local/mysql/data/localhost-slow.log |
+---------------------+-----------------------------------------+
1 row in set (0.01 sec)
</pre>
