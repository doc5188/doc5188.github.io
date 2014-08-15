---
layout: post
title: "linux 版快盘: kpfs (kuaipan FUSE filesystem)"
date: 2014-08-15 17:12:23
categories: 文件系统
tags: [linux, fuse, kpfs, filesystem]
---

作者联系方式：YU TAO <yut616 at sohu dot com>

关键字： 快盘，linux，ubuntu， open API，liboauth，json-c，fuse

近来看到 快盘 开放了 API，所以就基于 linux FUSE 实现了一个 filesystem，并作为 open source 开放出来，给大家使用。

代码位置：

http://code.google.com/p/kpfs/

C 语言，LGPL 。

有兴趣的可以下载使用。

kpfs是一款基于FUSE开发的用户空间文件系统，实现了在Linux中对快盘的基本操作。当文件系统挂载到Linux的某个文件夹下，用户只需像普通文件一样操作自己快盘中的目录和文件。

kpfs的特点

    基于FUSE的文件系统

    基于kuaipan.cn API

    使用了这些基础软件：liboauth, fuse, glib, curl, json-c

    支持gobject 反射，支持javascript和python绑定。

实现原理

KPFS通过FUSE来获取用户文件操作的指令，转而通过KPFS自行分装的文件操作函数，最终调用kuaipan.cn提供的API，实现对快盘文件的操作。 通过libcurl 库，来实现http报文的发送和接收，通过glib库实现KPFS文件系统inode节点的建立，查询，删除，插入。通过json-c库，实现对快盘服务器响应报文的解析。

























转载时请注明出处和作者联系方式：http://blog.csdn.net/mimepp
