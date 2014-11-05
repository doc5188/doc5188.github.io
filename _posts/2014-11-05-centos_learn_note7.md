---
layout: post
title: "第七天:centos6.5网卡查看命令"
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:24
---

<p>关于网卡的几个操作的命令：</P>
<p>&nbsp;<wbr>1.lsmod 查看网卡的模块是否加载，看看是否网卡驱动好了的意思</P>
<p>2. dmesg:查看是否检测到了网卡。</P>
<p>3.ifup ifdown 激活/停止网卡</P>
<p>4.ifconfig 查看网卡是否正常工作。 看看是否网卡有ip,有lo主机回还网络,表示设备没有问题。</P>
<p>windows下 查看的是 ipconfig /all 命令，centos下的&nbsp;<wbr> 是
ifcofnig 命令</P>
<p>ifconfig 接口</P>
<p>ifconfig eth0(接口) up/down&nbsp;<wbr> 激活网卡设备，网卡无效。</P>
<p>ifconfig eth0 netmask 255.255.254.0 设置掩码</P>
<p>ifconfig eth0&nbsp;<wbr> 192.168.0.21
设置eth0的ip地址为0.21</P>
<p>也可以写一行:ifconfig eth0 192.168.0.21 netmask 255.255.255.0</P>
<p>修改后需要重新启动网络设置:service network restart</P>
<p>5.看看网络是否相通</P>
<p>&nbsp;<wbr>ping -c 10（回显几次） ip/域名</P>
<p>eg: ping -c 192.168.1.1&nbsp;<wbr> 同 windows的一样。</P>
<p>6.如果上不了网，看下dns填写是否正确: /etc/resolv.conf文件。</P>
<p>7.上不去网的话：看看 默认路由设置错误，也会导致不能上网。</P>
<p>就设计到了route命令：</P>
<p>route 看下 default 的 网关 gateway
是不是你的路由器的ip地址，不是的话就上不了网，需要修改，如何修改呢？
先删除默认路由，这一条。然后再添加默认路由这一条。就可以了。</P>
<p>route del default</P>
<p>route add default gw
192.168.0.254(你的路由器的ip),需要root用户的身份才能操作.</P>
<p>&nbsp;<wbr></P>
