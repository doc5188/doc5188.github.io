---
layout: post
title: "Redhat/CentOS6.2 x86系统KVM虚拟机网络配置(一)—NAT方式"
categories: 虚拟化
tags: [kvm, qemu, 虚拟化, 虚拟机网络, NAT配置]
date: 2014-10-09 14:57:18
---

摘要：KVM虚拟机网络配置的两种方式：NAT方式和Bridge方式。NAT方式的配置原理和步骤。NAT方式适用于桌面主机的虚拟化。

* 问题

客户机安装完成后，需要为其设置网络接口，以便和主机网络，客户机之间的网络通信。事实上，如果要在安装时使用网络通信，需要提前设置客户机的网络连接。

KVM 客户机网络连接有两种方式：
<pre>
    用户网络（User Networking）：让虚拟机访问主机、互联网或本地网络上的资源的简单方法，但是不能从网络或其他的客户机访问客户机，性能上也需要大的调整。NAT方式。
    虚拟网桥（Virtual Bridge）：这种方式要比用户网络复杂一些，但是设置好后客户机与互联网，客户机与主机之间的通信都很容易。Bridge方式。
</pre>

本文主要解释NAT方式的配置。

* NAT方式原理

NAT方式是kvm安装后的默认方式。它支持主机与虚拟机的互访，同时也支持虚拟机访问互联网，但不支持外界访问虚拟机。

检查当前的网络设置：

{% highlight bash %}
# virsh net-list --all
Name State Autostart
-----------------------------------------
default active yes
{% endhighlight %}

default是宿主机安装虚拟机支持模块的时候自动安装的。

检查当前的网络接口：

{% highlight bash %}
# ifconfig
eth0      Link encap:Ethernet  HWaddr 44:37:E6:4A:62:AD  
          inet6 addr: fe80::4637:e6ff:fe4a:62ad/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:987782 errors:0 dropped:0 overruns:0 frame:0
          TX packets:84155 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:109919111 (104.8 MiB)  TX bytes:12695454 (12.1 MiB)
          Interrupt:17 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:4 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:240 (240.0 b)  TX bytes:240 (240.0 b)

virbr0    Link encap:Ethernet  HWaddr 52:54:00:B9:B0:96  
          inet addr:192.168.122.1  Bcast:192.168.122.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2126 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 b)  TX bytes:100387 (98.0 KiB)

virbr0-nic Link encap:Ethernet  HWaddr 52:54:00:B9:B0:96  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)
{% endhighlight %}

其中virbr0是由宿主机虚拟机支持模块安装时产生的虚拟网络接口，也是一个switch和bridge，负责把内容分发到各虚拟机。

几个虚拟机管理模块产生的接口关系如下图：

<img src="/upload/images/1337931226_5366.PNG" >

从图上可以看出，虚拟接口和物理接口之间没有连接关系，所以虚拟机只能在通过虚拟的网络访问外部世界，无法从网络上定位和访问虚拟主机。

virbr0是一个桥接器，接收所有到网络192.168.122.*的内容。从下面命令可以验证：

{% highlight bash %}
# brctl show
bridge name     bridge id               STP enabled     interfaces
virbr0          8000.525400b9b096       yes             virbr0-nic

# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.122.0   *               255.255.255.0   U     0      0        0 virbr0
{% endhighlight %}

同时，虚拟机支持模块会修改iptables规则，通过命令可以查看：

{% highlight bash %}
# iptables -t nat -L -nv
Chain PREROUTING (policy ACCEPT 16924 packets, 2759K bytes)
pkts bytes target     prot opt in     out     source               destination
Chain POSTROUTING (policy ACCEPT 2009 packets, 125K bytes)
pkts bytes target     prot opt in     out     source               destination        
 421 31847 MASQUERADE  all  --  *      *       192.168.122.0/24    !192.168.122.0/24   ----------->这条是关键，它配置了NAT功能。
Chain OUTPUT (policy ACCEPT 2011 packets, 125K bytes)
pkts bytes target     prot opt in     out     source               destination        

    
# iptables -t filter -L -nv
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination        
 1    74 ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0           udp dpt:53    ---->由libvirt脚本自动写入
 0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0           tcp dpt:53    ---->由libvirt脚本自动写入
 3   984 ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0           udp dpt:67    ---->由libvirt脚本自动写入
 0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0           tcp dpt:67    ---->由libvirt脚本自动写入
178K  195M ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED    ---->iptables的系统预设
 2   168 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0                ---->iptables的系统预设
1148  216K ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0                ---->iptables的系统预设
 1    60 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22  ---->iptables的系统预设
16564 2721K REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited ---->iptables的系统预设
Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target     prot opt in     out     source               destination        
3726 3485K ACCEPT     all  --  *      virbr0  0.0.0.0/0            192.168.122.0/24    state RELATED,ESTABLISHED  ---->由libvirt脚本自动写入
3491  399K ACCEPT     all  --  virbr0 *       192.168.122.0/24     0.0.0.0/0                ---->由libvirt脚本自动写入
 0     0 ACCEPT     all  --  virbr0 virbr0  0.0.0.0/0            0.0.0.0/0                ---->由libvirt脚本自动写入
 0     0 REJECT     all  --  *      virbr0  0.0.0.0/0            0.0.0.0/0           reject-with icmp-port-unreachable  ---->由libvirt脚本自动写入
 0     0 REJECT     all  --  virbr0 *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-port-unreachable  ---->由libvirt脚本自动写入
 0     0 REJECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0           reject-with icmp-host-prohibited  ---->iptables的系统预设
Chain OUTPUT (policy ACCEPT 181K packets, 138M bytes)
pkts bytes target     prot opt in     out     source               destination
{% endhighlight %}


如果没有default的话，或者需要扩展自己的虚拟网络，可以使用命令重新安装NAT。

* NAT方式的适用范围

桌面主机虚拟化。

创建步骤

{% highlight bash %}
# virsh net-define /usr/share/libvirt/networks/default.xml
{% endhighlight %}

此命令定义一个虚拟网络，default.xml的内容：

{% highlight bash %}
<network>
  <name>default</name>
  <bridge name="virbr0" />
  <forward/>
  <ip address="192.168.122.1" netmask="255.255.255.0">
    <dhcp>
      <range start="192.168.122.2" end="192.168.122.254" />
    </dhcp>
  </ip>
</network>
{% endhighlight %}

也可以修改xml，创建自己的虚拟网络。

标记为自动启动：

{% highlight bash %}
# virsh net-autostart default
Network default marked as autostarted
{% endhighlight %}

启动网络：

{% highlight bash %}
# virsh net-start default
Network default started
{% endhighlight %}

网络启动后可以用命令brctl show 查看和验证。

修改/etc/sysctl.conf中参数，允许ip转发：

net.ipv4.ip_forward=1


* 客户机安装

客户机安装时注意，网络要选择用NAT方式。

图形化的方式：

<img src="/upload/images/1337932930_9919.png" />

文本方式：

编辑修改虚拟机配置文件 /etc/libvirt/qemu/v1.xml，增加如下内容

{% highlight bash %}
    <interface type='network'>
      <mac address='52:54:00:4f:1b:07'/>
      <source network='default'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
{% endhighlight %}


虚拟机启动后，验证网络接口是否正常：

{% highlight bash %}
# brctl show
bridge name     bridge id               STP enabled     interfaces
virbr0          8000.525400b9b096       yes             virbr0-nic
                                                                                 vnet0
{% endhighlight %}

Bridge方式的影响

Bridge方式配置出来的接口对NAT方式没有影响，因为NAT方式并没有使用物理网卡。但作为客户机，只能选择其中的一种。 
