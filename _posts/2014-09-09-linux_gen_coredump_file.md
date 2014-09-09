---
layout: post
title: "Linux下如何产生coredump（gdb调试用）"
categories: linux
tags: [coredump, gdb]
date: 2014-09-09 13:07:21
---
任务发生异常，需要记录遗言信息，利用gdb调试，因此需要记录coredump文件。

设置查看：

在root用户下执行sysctl -a | grep core，查看core文件的配置是否正确

命令设置：

1）使用命令 ulimit -c unlimited 设置coredump文件可以使用最大空间；

　　或去vi /etc/security/limits.conf修改

2）/proc/sys/kernal/core_pattern 可以设置coredump产生的路径和文件名格式。如果不修改，默认在程序执行目录下产生。

 　　或使用命令修改：

　　　　sysctl -w kernel.core_pattern=/core/core.%e.%p

如果设置了上述两点，还是不能产生coredump，可能是以下原因：

1） 有些信号量默认是不产生coredump的，可以用 man signal  看一下。

2） 硬盘空间不够了，coredump需要占用很大的硬盘空间（上G的空间）；

3） ulimit -c 命令只在当前terminal上有效，也就是程序启动的terminal设置该命令才有效。该命令无效，当然就不能产生coredump了。

