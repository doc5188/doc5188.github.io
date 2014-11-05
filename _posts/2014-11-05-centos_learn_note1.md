---
layout: post
title: "第十三天:centos6.5的网卡的设置."
categories: linux
tags: [centos学习教程, 系列教程]
date: 2014-11-05 10:06:18
---

<p>1.修改主机名称：</P>
<p>配置文件为： /etc/sysconfig/network, 使用 hostname 显示主机名称。带参数可以修改</P>
<p>2.修改ip,方法很多: setup命令，刚装系统的时候，ifconfig eth0 ip netmask等。</P>
<p>配置文件：/etc/sysconfig/network-scripts/ifcfg-eth0,有以下几个选项：</P>
<p>&nbsp;<wbr><br />
DEVICE=eth0 网卡名称<br />
HWADDR=00:15:17:b3:fd:83 mac地址<br />
TYPE=Ethernet<br />
UUID=c5354aa5-aabd-4142-bb15-da9145fdc047<br />
ONBOOT=yes 系统启动时是否 启动<br />
NM_CONTROLLED=yes<br />
BOOTPROTO=static&nbsp;<wbr> 启动方式。有dhcp
静态ip设置,首次安装的时候网卡不启动，就是这个原因，这里需要修改为静态ip才可以.</P>
<p>IPADDR=192.168.0.238 我这台机器的ip设置<br />
NETMASK=255.255.255.0<br />
GATEWAY=192.168.0.254<br />
DNS1=219.149.6.99<br />
IPV6INIT=no<br />
USERCTL=no<br />
3.dns修改：</P>
<p>文件: /etc/resolv.conf 每行添加即可</P>
<p>4.ifconfig命令 查看设置。</P>
<p>5.service network restart .</P>
<p>&nbsp;<wbr></P>
