---
layout: post
title: "后台运行 MongoDB 服务进程 mongod"
categories: 数据库
tags: [mongod服务进程]
date: 2014-10-09 23:17:37
---

 在 UNIX/Linux 系统中，通过 ./bin/mongod 启动 MongoDB 服务时，屏幕会输出很多运行信息，并不会回到 shell 提示符。除非 Ctrl + C，但是这样会停止 MongoDB 服务进程。

那么如何使 MongoDB 后台运行呢？可以使用下面的办法：

<pre>
# 方法1：(推荐)
# --fork 选项将会通知 mongod 在后台运行
/path/to/MongoDB_Dir/bin/mongod --logpath /path/to/file.log --logappend --fork
 
# 方法2：
# 将输出重定向到 file.log 文件
# & 将该进程置于后台运行
/path/to/MongoDB_Dir/bin/mongod >> /path/to/file.log &
 
# 还可以这样运行(不记录日志)
# 因为所有重定向到位桶文件 /dev/null 的信息都会被丢弃
/path/to/MongoDB_Dir/bin/mongod >> /dev/null &

</pre>
