---
layout: post
title: "Linux访问Windows共享文件夹"
categories: linux
tags: [linux]
date: 2015-02-12 16:13:01
---

Linux 访问 Windows 共享文件夹

 

下文一些东西来自于网络， 不过更重要的是加入自己配置过程中的一些经历， 把自己经历的 错误和解决方法分享给大家。 
 

环境： Linux 

 VMWare 虚拟机， Ubuntu12.04 

Windows Windows7 

 

操作：

 

 

从 Linux 中访问 Windows 的共享文件 

在 Linux 命令行下输入下列命令：

 

<pre>
# mount -t smbfs -o username=user,password=pwd //192.168.xx.xx/share /mnt/winshare
</pre>

smbfs ，文件系统类型

username ，访问机器的用户名

password ，访问机器用户名的密码

//192.168.xx.xx/share ，访问机器的的

ip 和共享的文件夹名称

 

/mnt/winshare ， Linux 中挂载要访问的目录

 

请注意，用户名和密码的逗号之间不能有空格

 

 

利用该命令可能会出现提示不认识 smbfs 文件系统的错误。现在 Linux 已经用 cifs 替代 smbfs ，所以上面的命令可以修改为如下命令： 
 
<pre>

# mount -t cifs -o username=user,password=pwd //192.168.xx.xx/share 
</pre>

 

/mnt/winshare 敲回车后如果没有任何提示说连接成功

 

请注意，如果密码输入错误，或者没有写密码选项有可能会提示如下错误：

 

<pre>
mount: block device //192.168.xx.xx/share is write-protected, mounting read-only 

mount: cannot mount block device //192.168.xx.xx/share read-only
</pre>

 

 

在连接过程中如果出现

mount:Connection refuse 的错误，请注意有可能是你连接 windows 实体机的 IP 写错了，不要写虚拟机的网关，要写 VMWare 实体机的 IP 。 
 

例如， VMWare 的默认网关为 192.168.95.2 ， erVMWare 实体机的 Ip 是 192.168.95.1 

 

umount 卸载

 

<pre>
# umount /mnt/winshare 
</pre>

或

 

<pre>
# umount //192.168.xx.xx/share 
</pre>

 

注意卸载前要离开

 

/mtn/share 目录，否则会显示 "device is busy" 。

  
