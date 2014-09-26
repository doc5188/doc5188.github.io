---
layout: post
title: "linux 版快盘: kpfs (kuaipan FUSE filesystem)"
date: 2014-08-15 17:12:23
categories: 文件系统
tags: [linux, fuse, kpfs, filesystem, 开源项目]

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

kpfs 是 linux 下基于 FUSE 的 filesystem。

目前需要自己下载并编译，并配置 kpfs.conf 信息。
代码下载地址：
http://code.google.com/p/kpfs/downloads/list

卸载使用类似下面的命令：
fusermount -u /tmp/kpfs

【截图】

kuaipan 网站上，原始目录信息：

<img src="/upload/images/medium.jpg" />

oauth 过程：

<img src="/upload/images/OPbTo.png" />

需要配置的 kpfs.conf

<img src="/upload/images/8cs1D.png" />

外层目录信息：

<img src="/upload/images/4tEYK.png" />

shell 中查看目录信息：

<img src="/upload/images/pqLJJ.png" />

使用 find 命令列出全部文件：

<img src="/upload/images/11FQNP.png" />

在文件管理器中查看目前文件：

<img src="/upload/images/ALfCx.png" />

在文件管理器中查看目录属性：

<img src="/upload/images/jm7KS.png" />

在浏览器中查看目录：

<img src="/upload/images/MDaFF.png" />

自己动手，丰衣足食。
Just for fun

2012-03-29 更新
read 可以工作了，能看到图片的 thunbmail 了，music/video 可以播放，也可以拖动快进了。
读取文件：

<img src="/upload/images/fzNQo.png" />

音乐播放：

<img src="/upload/images/nrRsZ.png" />

文件管理器中，自动显示缩略图，不需要使用 thumbnail API：

<img src="/upload/images/I2uFI.png" />

文本也有缩略图，README 上的文字就是：

<img src="/upload/images/RHHwT.png" />

用 mplayer 播放 video，就是太卡了点。

<img src="/upload/images/medish.jpg" />


中文目录好了，但需要 liboauth-0.9.5 以上版本的支持。

<img src="/upload/images/fs04B.png" />

2012-04-01 增加 statfs 方法

<img src="/upload/images/dPHlz.png" />


2012-04-16
增加 write 方法，目前文件可以读写了。
2012-08-22
增加 gobject introspection 功能，从而实现多语言绑定，如 javascript, python。

<img src="/upload/images/GVO8p.png" />




















转载时请注明出处和作者联系方式：http://blog.csdn.net/mimepp


