---
layout: post
title: "在 Ubuntu 12.04 上安装 Open vSwitch"
categories: linux
tags: [linux, openvswitch]
date: 2014-08-27 17:13:23
---

   云计算时代人类已经成功虚拟化了服务器硬件，现在大大小小的数据中心有无数的虚拟机跑在服务器硬件上，看上去很美好，但是任务还没有完成，这么多的虚拟机都依赖物理服务器（所在）的网络端口、网络和交换机（除了物理依赖还依赖这些硬件上的软件配置），这让底层变动成为一个大问题，比如我们想改变服务器 A 上的网络设置（192.168.2.0 改成 172.16.2.0）或者物理移动服务器 A 到另一数据中心，那么服务器 A 上运行的虚拟机怎么办呢？逐个改动配置是很麻烦的。有没有一种办法能把虚拟机所在的网络和物理服务器的网络隔开呢（虽然可以用 VLAN，但是还是不够）？这正是网络虚拟化正在做的，通过软件的方式形成交换机部件（vSwitch），让各个虚拟机和虚拟交换机连接起来而不用去理会真实物理机和物理交换机。比如，让 Host A 上的 VM02 和 Host B 上的虚拟机 VM10 连成一个网络而不用理会虚拟机（VM）所在服务器（Host）的网络设置。

网络虚拟化或者软件定义网络（Software Defined Network, SDN）的应用远不止这些，任何了解 SDN 的人都不会怀疑 SDN 的未来，这也是为啥 VMware 愿意花12亿美金买 Nicira（软件定义网络的先驱）。

要使用 SDN/OpenFlow 就必须有支持 OpenFlow 协议的物理（或软件）交换机，OpenvSwitch 就是这么一个支持 OpenFlow 协议的开源虚拟交换机。我们从安装虚拟交换机 Open vSwitch 开始来慢慢了解网络虚拟化吧。

安装必要软件包：

{% highlight bash %}
$ sudo -i
# apt-get install kvm libvirt-bin openvswitch-controller openvswitch-brcompat openvswitch-switch openvswitch-datapath-source
{% endhighlight %}

启动 Open vSwitch 服务，如果报错 FATAL: Error inserting brcompat_mod 模块错误则需要编译和加载 brcompat_mod 这个模块，这个模块是 openvswitch 为了兼容 linux bridge 而来的，有些程序使用 Linux bridge（比如 brctl），这些程序为了能在 openvswitch 下继续使用将需要这个 brcompat_mod 兼容模块，这个模块为那些慢慢迁移到 openvswitch 的程序提供了方便：

{% highlight bash %}
# service openvswitch-switch start
FATAL: Error inserting brcompat_mod (/lib/modules/3.2.0-30-generic/updates/dkms/brcompat_mod.ko): Invalid module format
 * Inserting brcompat module
Module has probably not been built for this kernel.
For instructions, read
/usr/share/doc/openvswitch-datapath-source/README.Debian
FATAL: Error inserting brcompat_mod (/lib/modules/3.2.0-30-generic/updates/dkms/brcompat_mod.ko): Invalid module format
 * Inserting brcompat module

# module-assistant auto-install openvswitch-datapath
{% endhighlight %}

编译模块后再次尝试启动服务：

{% highlight bash %}
# service openvswitch-switch restart
 * Killing ovs-brcompatd (1606)
 * Killing ovs-vswitchd (1603)
 * Killing ovsdb-server (1594)
 * Starting ovsdb-server
 * Configuring Open vSwitch system IDs
 * Starting ovs-vswitchd
 * Starting ovs-brcompatd
 * iptables already has a rule for gre, not explicitly enabling

 # service openvswitch-controller restart
 * Restarting ovs-controller ovs-controller                                              Sep 12 13:46:46|00001|stream_ssl|INFO|Trusting CA cert from /etc/openvswitch-controller/cacert.pem (/C=US/ST=CA/O=Open vSwitch/OU=switchca/CN=OVS switchca CA Certificate (2012 Sep 12 13:42:19)) (fingerprint 46:5b:14:1f:13:56:b0:b0:a7:4d:10:39:ee:68:18:d4:39:3c:4b:d0)
                                                                                  [ OK ]
{% endhighlight %}

编辑配置文件，取消注释并设置 BRCOMPAT 为 yes 以便启动后能使用 brcompat_mod 模块：
{% highlight bash %}
# vi /etc/default/openvswitch-switch
# This is a POSIX shell fragment                -*- sh -*-

# FORCE_COREFILES: If 'yes' then core files will be enabled.
# FORCE_COREFILES=yes

# BRCOMPAT: If 'yes' and the openvswitch-brcompat package is installed, then
# Linux bridge compatibility will be enabled.
BRCOMPAT=yes
{% endhighlight %}

重启一下系统，验证一下是否模块被自动加载：

{% highlight bash %}
# reboot
{% endhighlight %}

{% highlight bash %}
# lsmod | grep brcom
brcompat_mod           13512  0 
openvswitch_mod        83993  1 brcompat_mod

使用 openvswitch 增加网桥 br0 并把网络接口 eth0 加入 br0：

# ovs-vsctl add-br br0
# ovs-vsctl add-port br0 eth0

# ovs-vsctl show          
a23c503b-bfbe-4646-8738-a7f69e5d69a0
    Bridge "br0"
        Port "eth0"
            Interface "eth0"
        Port "br0"
            Interface "br0"
                type: internal
    ovs_version: "1.4.0+build0"
{% endhighlight %}

配置网桥 br0 和网络接口 eth0（和用 bridge-utils 工具配置的时候一样，不同的是这里用更先进的 openvswitch/brcompat_mod 替换了 bridge-utils）：

{% highlight bash %}
# ifconfig eth0 0
# ifconfig br0 192.168.2.45 netmask 255.255.255.0
# route add default gw 192.168.1.1 br0
{% endhighlight %}

为了保存网络设置，最好把上面的配置写到 /etc/network/interfaces 里：

{% highlight bash %}
# vi /etc/network/interfaces
auto lo
iface lo inet loopback

auto br0
iface br0 inet static
address 192.168.2.45
netmask 255.255.255.0
gatew
{% endhighlight %}
