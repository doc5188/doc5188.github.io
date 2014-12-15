---
layout: post
title: "device eth0 does not seem to be present, delaying initialization"
categories: linux
tags: [linux]
date: 2014-12-15 10:57:20
---

vmlite虚拟机启动出错，就把这个虚拟机删除掉重新建立，系统虚拟硬盘使用之前的，启动系统后不能上网，通过ifconfig查看网卡没启动，遂启动网卡服务，但是出错，就是：device eth0 does not seem to be present, delaying initialization，然后想到是不是ifcfg-eth0的配置文件里保存了以前的MAC地址，就把这一行删除掉在重启网卡，还是一样的错误，随后网上查了下资料，把/etc/udev/rules.d/70-persistent-net.rules 删除后重启机器就可以了，因为这个文件绑定了网卡和mac地址，所以换了网卡以后MAC地址变了，所以不能正常启动，也可以直接编辑这个配置文件把里面的网卡和mac地址修改乘对应的，不过这样多麻烦，直接删除重启，它会自动生成个。

1、

vi /etc/sysconfig/network-scripts/ifcfg-eth0

ifcfg-eth0的配置文件里保存了以前的MAC地址，就把这一行删除掉在重启网卡

2、

/etc/udev/rules.d/70-persistent-net.rules 删除后重启机器

因为这个文件绑定了网卡和mac地址，所以换了网卡以后MAC地址变了，所以不能正常启动，也可以直接编辑这个配置文件把里面的网卡和mac地址修改乘对应的，不过这样多麻烦，直接删除重启，它会自动生成个。
