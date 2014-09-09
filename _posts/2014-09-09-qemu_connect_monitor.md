---
layout: post
title: "qemu连接到监视器-qemu connect monitor"
date: 2014-09-09 15:23:21
categories: linux
tags: [linux, qemu, kvm, qemu-monitor]
---

这是一个很实用的功能，因为在convirt的配置中需要更换光盘镜像文件，当时在convirt中操作的时候，好像是有一些问题，导致我必需重启这台虚拟机才可以让更换生效，然后想到在qemu的GUI中是可以通过alt+F2切换到监视器去用change命令更换光盘镜像的。难道qemu通过deamon模式运行是不能连接到监视器的么？不会的，强大的qemu是不会让我失望的。在google之后，终于发现了如下方法： 启动qemu的时候，需要加如下参数：-monitor unix:/var/run/kvm/monitors/vir-1,server,nowait  #这行的意思是把监视器放在/var/run/kvm/monitors/vir-1这个socket上，然后我们就可以通过nc -v -U /var/run/kvm/monitors/vir-1 来连接到这个socket上，这样就可以使用监视器啦，哈哈，注意一点是nc的版本，在nc.openbsd版本中是提供-U的参数的，其他某个版本是不提供的，大家要注意。

<pre>
源：
http://lishuai860113.blog.163.com/blog/static/8907094201142093356634/
</pre>
