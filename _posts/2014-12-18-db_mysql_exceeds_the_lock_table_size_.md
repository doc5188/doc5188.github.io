---
layout: post
title: "Mysql exceeds the lock table size"
categories: 数据库 
tags: [mysql, mysql exceeds]
date: 2014-12-18 17:52:33
---

故障现象

<pre>
    mysql> delete FROM `tablesname` WHERE datetime<'2009-03-06';  
    ERROR 1206 (HY000): The total number of locks exceeds the lock table size  
</pre>


解决步骤

1、锁表写操作

<pre>
    mysql> lock tables tablesname write;  
    mysql> delete FROM `tablesname` WHERE datetime<'2009-03-06';  
    ERROR 1206 (HY000): The total number of locks exceeds the lock table size  
</pre>


没有解决。

2、 innodb修改改innodb_buffer_pool_size值(一般配置为总内存的30%-40% ) myisam修改key_buffer(若是myisam应该没这个问题,因为myisam不是行级锁)

重启Mysql，解决。

<pre>
referer:http://blog.liuts.com/post/140/
</pre>
