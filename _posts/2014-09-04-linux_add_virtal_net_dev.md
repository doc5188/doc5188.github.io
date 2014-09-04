---
layout: post
title: "给centos vps添加额外的ip"
categories: linux
tags: [linux, centos, 虚拟网卡, VPS]
date: 2014-09-04 17:55:21
---

给centos vps添加额外的ip

Posted by yar999 in Linux技术 on 2010/11/18 with No Comments

本文介绍怎样给CentOS的VPS或者独立主机增加新的IP地址。

增加新IP需要知道的是新的IP地址和子网掩码，其他信息（比如网关）都不再需要了。假如需要增加的ip是177.252.202.179，子网掩码是255.255.255.248

在目录/etc/sysconfig/network-scripts/ 下面是一些网卡的配置文件，新增加一个额外IP地址，需要在这个目录下新增加一个新网卡配置文件。额外IP的网卡配置文件的文件名是有要求的，必须是ifcfg-eth0:XXXX的形式，其中eth0代表物理网卡，eth0:XXXX 代表是附加在这个物理网卡上的虚拟网卡，XXXX可以是1到4位的字符串，字符串内容可以包含任意字母和数字。

ssh登录到centos之后

<pre>
cd /etc/sysconfig/network-scripts/
vi ifcfg-eth0:1
</pre>

然后输入下面的内容
<pre>
DEVICE=eth0:1
BOOTPROTO=static
IPADDR=177.252.202.179
NETMASK=255.255.255.248
ONBOOT=yes
</pre>

然后保存退出，执行

ifup eth0:1

就可以启用177.252.202.179这个新增的ip

如果您需要增加第二个ip，您可以执行

vi ifcfg-eth0:2

然后输入，下面的内容

<pre>
DEVICE=eth0:2
BOOTPROTO=static
IPADDR=177.252.202.179
NETMASK=255.255.255.248
ONBOOT=yes
</pre>

然后执行下面的命令，启用177.252.202.179这个ip

ifup eth0:2
注意:

网卡配置文件中的变量名例如DEVICE等等，都需要大写。配置不同的网卡只需要修改
DEVICE(设备名字) IPADDR(ip地址) NETMASK(子网掩码)这3项就可以了


