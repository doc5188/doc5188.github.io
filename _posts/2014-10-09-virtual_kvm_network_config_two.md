---
layout: post
title: "Redhat/CentOS6.2 x86系统KVM虚拟机网络配置(二)—Bridge方式"
categories: 虚拟化
tags: [kvm, qemu, 虚拟化, 虚拟机网络, Bridge配置]
date: 2014-10-09 15:07:18
---


摘要：KVM虚拟机网络配置的两种方式：NAT方式和Bridge方式。Bridge方式的配置原理和步骤。Bridge方式适用于服务器主机的虚拟化。

* 问题

客户机安装完成后，需要为其设置网络接口，以便和主机网络，客户机之间的网络通信。事实上，如果要在安装时使用网络通信，需要提前设置客户机的网络连接。

KVM 客户机网络连接有两种方式：
<pre>
    用户网络（User Networking）：让虚拟机访问主机、互联网或本地网络上的资源的简单方法，但是不能从网络或其他的客户机访问客户机，性能上也需要大的调整。NAT方式。
    虚拟网桥（Virtual Bridge）：这种方式要比用户网络复杂一些，但是设置好后客户机与互联网，客户机与主机之间的通信都很容易。Bridge方式。
</pre>

本文主要解释Bridge方式的配置。

* Bridge方式原理

Bridge方式即虚拟网桥的网络连接方式，是客户机和子网里面的机器能够互相通信。可以使虚拟机成为网络中具有独立IP的主机。

桥接网络（也叫物理设备共享）被用作把一个物理设备复制到一台虚拟机。网桥多用作高级设置，特别是主机多个网络接口的情况。

<img src="/upload/images/1338191713_7431.PNG" />

如上图，网桥的基本原理就是创建一个桥接接口br0，在物理网卡和虚拟网络接口之间传递数据。


* Bridge方式的适用范围

服务器主机虚拟化。

* 网桥方式配置步骤

1、编辑修改网络设备脚本文件，增加网桥设备br0

{% highlight bash %}
vi /etc/sysconfig/network-scripts/ifcfg-br0
DEVICE="br0"
ONBOOT="yes"
TYPE="Bridge"
BOOTPROTO=static
IPADDR=10.0.112.39
NETMASK=255.255.255.0
GATEWAY=10.0.112.1
DEFROUTE=yes
{% endhighlight %}

上述配置将虚拟网卡配置在了10.0.112.* 网段。如果不需要静态地址，可以把配置地址的相关项屏蔽。如：

{% highlight bash %}
DEVICE="br0"
ONBOOT="yes"
TYPE="Bridge"
BOOTPROTO=dhcp
{% endhighlight %}


2、编辑修改网络设备脚本文件，修改网卡设备eth0

{% highlight bash %}
DEVICE="eth0"
NM_CONTROLLED="no"
ONBOOT="yes"
TYPE=Ethernet
BOOTPROTO=none
BRIDGE="br0"
NAME="System eth0"
HWADDR=44:37:E6:4A:62:AD
{% endhighlight %}

NM_CONTROLLED这个属性值，根据redhat公司的文档是必须设置为“no”的（这个值为“yes”表示可以由服务NetworkManager来管理。NetworkManager服务不支持桥接，所以要设置为“no”。），但实际上发现设置为“yes”没有问题。通讯正常。

3、重启网络服务

{% highlight bash %}
# service network restart
{% endhighlight %}

4、校验桥接接口

{% highlight bash %}
# brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.4437e64a62ad       no              eth0
{% endhighlight %}


客户机配置

客户机安装时注意，网络要选择用br0桥接方式。

图形化的方式：

<img src="/upload/images/1338197249_7016.png" />


文本方式：

编辑修改虚拟机配置文件 /etc/libvirt/qemu/v1.xml，增加如下内容

{% highlight bash %}
    <interface type='bridge'>
      <mac address='52:54:00:da:c3:dc'/>
      <source bridge='br0'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>
{% endhighlight %}


虚拟机启动后，验证网络接口是否正常：

{% highlight bash %}
# brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.4437e64a62ad       no              eth0
                                                        vnet0
{% endhighlight %}

* NAT方式的影响

网桥方式的配置与虚拟机支持模块安装时预置的虚拟网络桥接接口virbr0没有任何关系，配置网桥方式时，可以把virbr0接口（即NAT方式里面的default虚拟网络）删除。

{% highlight bash %}
# virsh net-destroy default
# virsh net-undefine default
# service libvirtd restart
{% endhighlight %}


