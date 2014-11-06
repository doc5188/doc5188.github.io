---
layout: post
title: "ssh_exchange_identification: Connection closed by remote host"
categories: linux
tags: [ssh_exchange_identification]
date: 2014-11-06 09:26:47
---

<pre>

花了两个星期。
终于搞定ssh_exchange_identification: Connection closed by remote host

走了许多弯路。
写解决方法
主要是 /etc/hosts.allow 和 ／etc/hosts.deny问题 最好两个都设置一下。
因为有些系统是先load hosts.allow 再 load hosts.allow .有些相反。
hosts.allow:
ALL:ALL:allow sshd sshd1 sshd2:ALL:allow #ssh:0.0.0.0/0.0.0.0 sshd:192.168.1.:allow hosts.deny sshd[2760]:
# you should know that NFS uses portmap!
ALL:ALL EXCEPT 127.0.0.1:DENY to ALL:ALL EXCEPT 127.0.0.1 AND 192.168.1.111:DENY

完成后。重启sshd :
service sshd restart     /etc/init.d/sshd restart

如果还不行就查一下syslog

位置在 /var/log/syslog
在那可以看到为什么不行。再改一下。再测试一下。反正都要多试几种方法
....
....refused connect from ::ffff:192.168.*.*...
.........

上个星期去 google查的时候发再外国有位仁兄，超搞笑。他出现这个问题后。也搞了很久，但是还不行。然后他就不想理它了，出去玩。回来后就可以连接上了。于是我想我也把网线拔了。等了两天发现还是不行啊。所以说外国的经验还是不能照套的。

我在想，上baidu找一下吧，发现只有提问的。没有回答的。百度知道根本都没有这个问题。只能上google了，还好，找到了一些眉目，于是就尝试锁定hosts。全英对我没有什么问题，外语大学的嘛，找找看。设置一下，
发现sshd_conf是没问题的。
记得重点放要在hosts.allow和hosts.deny那。

并且log日志很重要的。所以我也看了大半天的网上日志资料。(用google查)

</pre>
