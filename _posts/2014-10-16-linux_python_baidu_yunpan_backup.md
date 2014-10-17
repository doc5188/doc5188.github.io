---
layout: post
title: "Linux下百度云的Python客户端（支持Unicode）"
categories: linux
tags: [百度云python客户端]
date: 2014-10-16 23:51:12
---

bypy - 百度云/百度网盘的Python客户端

下载地址：

https://github.com/houtianze/bypy

Copyright 2013 Hou Tianze (GitHub: houtianze, Twitter: @ibic, G+: +TianzeHou)

这是一个百度云/百度网盘的Python客户端。主要的目的就是在Linux环境下（命令行）使用百度云盘的2TB的巨大空间。比如，你可以用在Raspberry Pi树莓派上。它提供文件列表、下载、上传、比较、向上同步、向下同步，等等。

全面支持Unicode / 中文。错误重试，递归上/下载，目录比较，哈希缓存。

界面是英文的，主要是因为这个是为了Raspberry Pi树莓派开发的。

第一次运行的时候要通过百度的网页进行授权（一次就好）

 

重要1 想要支持中文，你要把系统的区域编码（locale）设置为UTF-8。

重要2 你需要安装Python Requests 库. 在 Debian / Ubuntu / Raspbian 环境下，只需执行如下命令一次：

sudo pip install requests

上手：

显示使用帮助和所有命令（英文）:

bypy.py

更详细的了解某一个命令：

bypy.py help 

显示在云盘（程序的）根目录下文件列表：

bypy.py list

把当前目录同步到云盘：

bypy.py syncup

or

bypy.py upload

把云盘内容同步到本地来：

bypy.py syncdown

or

bypy.py downdir /

比较本地当前目录和云盘（程序的）根目录（这个很有用）：

bypy.py compare 

还有一些其他命令 ...

哈希值的计算加入了缓存处理，使得第一次以后的计算速度有所提高。

运行时添加 -v 参数，程序会显示进度详情；添加 -d ，程序会显示一些调试信息。
