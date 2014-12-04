---
layout: post
title: "用Pyinstaller建立linux下Python的独立可执行文件"
categories: linux
tags: [python, linux, pyinstaller]
date: 2014-12-04 13:16:18
---

以下内容假定已安装好Python 2.4/2.5<br>
<br>
<strong>一、下载并编译pyinstaller</strong>（只需做一次，以后可直接做第二步）<br>
<br>
<strong>1.下载pyinstaller,现在的版本是1.3</strong><br>
(1)wget <a href="http://pyinstaller.hpcf.upr.edu/source/1.3/pyinstaller_1.3.tar.gz" target="_blank">http://pyinstaller.hpcf.upr.edu/source/1.3/pyinstaller_1.3.tar.gz</a><br>
<br>
<strong>2.解包进入源码目录</strong><br>
(1)tar zxv pyinstaller_1.3.tar.gz<br>
(2)cd pyinstaller-1.3/source/linux<br>
<br>
<strong>3.编译源代码</strong><br>
(1)python Make.py&nbsp;&nbsp;生成python的 .pyc文件<br>
<br>
如无错误，则出现如下提示（只有一行）：<br>
Now run "make" to build the targets: ../../support/loader/run ../../support/loader/run_d<br>
<br>
(2)make 连接生成linux的 .o 文件<br>
<br>
<strong>4.生成编译配置文件</strong><br>
(1)python Configure.py&nbsp;&nbsp;生成config.dat配置文件<br>
<br>
<br>
<strong>二、编译独立运行的python可执行文件</strong><br>
<br>
<strong>1.生成spec文件</strong><br>
python pyinstaller-1.3/Makespec.py --onefile --upx linuxlaptop.py<br>
<br>
参数说明：<br>
--onefile 生成单文件<br>
--upx&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;生成压缩的文件（可减小执行文件体积，需先安装upx软件包）<br>
<br>
<br>
<strong>2.生成最终的可执行文件</strong><br>
python pyinstaller-1.3/Build.py linuxlaptop.spec<br>
<br>
执行完成后将在当前目录生成可执行的linuxlaptop文件，如有问题欢迎与我交流：linuxlaptop.cn。<br>

