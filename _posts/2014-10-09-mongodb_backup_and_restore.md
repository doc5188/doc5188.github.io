---
layout: post
title: "mongodb数据库的备份与恢复"
categories: 数据库
tags: [mongodb数据备份, mongodb]
date: 2014-10-09 23:15:20
---

不用多想，数据的备份无论什么时候都是必须的，尤其是重要数据。

先介绍下命令语法：
<pre>
./mongodump -h 127.0.0.1:10001 -d lietou -o /usr/local/data

-h：MongDB所在服务器地址，例如：127.0.0.1，当然也可以指定端口号：127.0.0.1:10001

-d：需要备份的数据库实例，例如：lietou

-o：备份的数据存放位置，例如：/usr/local/data ，在备份完成后，系统自动在dump目录下建立一个lietou目录，这个目录里面存放该数据库实例的备份数据。
</pre>

* 数据库还原
<pre>
./mongorestore -h 127.0.0.1:10001 -d test  --directoryperdb /usr/local/data/lietou/

h：MongoDB所在服务器地址

-d：需要恢复的数据库实例，例如：test，当然这个名称也可以和备份时候的不一样，比如test2

--directoryperdb：备份数据所在位置，例如：/usr/local/data/lietou/，这里为什么要多加一个lietou，而不是备份时候的dump，读者自己查看提示吧！

--drop：恢复的时候，先删除当前数据，然后恢复备份的数据。就是说，恢复后，备份后添加修改的数据都会被删除，慎用哦！

</pre>
