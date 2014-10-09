---
layout: post
title: "linux ssh连接慢"
categories: linux
tags: [linux, ssh]
date: 2014-10-09 17:39:06
---

最近发现ssh连接的时候却很慢，ping的速度非常好，让人误以为是ssh连接不上。

分析结果，主要原因为：DNS的解析IP导致，可分别使用以下几种分析处理方式

1、在server上/etc/hosts文件中把你本机的ip和hostname加入　

2、在server上/etc/ssh/sshd_config文件中修改或加入UseDNS=no　

3、注释掉server上/etc/resolv.conf中不使用的IP所有行　

4、修改server上/etc/nsswitch.conf中hosts为hosts：files

5、authentication gssapi-with-mic也有可能出现问题，在server上/etc/ssh/sshd_config文件中修改 GSSAPIAuthentication no。/etc/init.d/sshd restart重启sshd进程使配置生效。

如之前为服务器配置了双网卡，使的在/etc/resolv.conf文件中多了一行目前不使用的IP地址。注释或者删除该行即可。大多数情况修改1和5两项即可解决问题

==================================

使用ssh -v dest_ip查看是在什么地方慢的，结果是问题5，google后有人提议把$HOME/.ssh目录权限修改为700，该目录下的文件权限也修改为只有本人可以访问，但问题依然存在。按照5中方法修改后问题解决。

另外，服务器无法连接外网，把/etc/resolv.conf中的nameserver全部注释掉，问题也能解决。使用strace查看后发现，ssh在验证完key之后，进行authentication gssapi-with-mic，此时先去连接DNS服务器，在这之后会进行其他操作。

--------------------------------------------------------------------

根据上述问题进行排查，发现是

3、注释掉server上/etc/resolv.conf中不使用的IP所有行　
的问题

因为在一开始安装linux的时候，该配置文件被设置。


